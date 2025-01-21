from utils.llm_api.client import HuggingFaceLLMClient, GPT4AllClient
from utils.llm_api.query import QueryProvider, QueryType
import json
import logging
from typing import Union
import re
import io
import geopandas as gpd
## needed for running solution
import matplotlib.pyplot as plt
import shapely
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import scipy
import sklearn
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def clean_python_code(code_string):
    """
    Removes comments, import statements, and print statements from a Python code string.
    """
    # Remove comments (single-line and multi-line)
    code_string = re.sub(r'#.*', '', code_string)  # Single-line comments
    code_string = re.sub(r'""".*?"""|\'\'\'.*?\'\'\'', '', code_string, flags=re.DOTALL)  # Multi-line comments

    # Remove import statements
    code_string = re.sub(r'^\s*import .*|^\s*from .* import .*', '', code_string, flags=re.MULTILINE)

    # Remove print statements
    code_string = re.sub(r'^\s*print\(.*\)\s*$', '', code_string, flags=re.MULTILINE)

    # Remove empty lines caused by the removals
    code_string = re.sub(r'\n\s*\n', '\n', code_string)

    return code_string.strip()

def get_description_extraction_function_string(cleaned_transform_code: str) -> str:
    get_transformed_data_description_header = "def get_transformed_data_description(data_gdf: gpd.GeoDataFrame) -> str:"
    description_extraction_code = """\n\tbuffer = io.StringIO()\n\ttransformed_data.info(buf=buffer)\n\tintermediate_data_description = buffer.getvalue()\n\treturn intermediate_data_description
    """

    description_extraction_function = (
        get_transformed_data_description_header + 
        '\n\t' + cleaned_transform_code.replace('\n', '\n\t') + 
        description_extraction_code
    )
    return description_extraction_function

def get_solution_function_string(cleaned_transform_code: str, cleaned_visualize_code: str) -> str:
    get_transformed_data_description_header = "def solve(data_gdf: gpd.GeoDataFrame, europe_gdf: gpd.GeoDataFrame):"

    function_body = (
        get_transformed_data_description_header + 
        '\n\t' + cleaned_transform_code.replace('\n', '\n\t') + 
        '\n\t' + cleaned_visualize_code.replace('\n', '\n\t')
    )
    
    return function_body

def extract_python_code(response: str) -> str:
    response = response.split("```python")
    if len(response) > 1:
        response = response[1].split("```")
        return response[0].strip()
    return response.strip()

def extract_json(response: str) -> str:
    response = response.split("```json")
    if len(response) > 1:
        response = response[1].split("```")
        return json.loads(response[0].strip())
    return json.loads(response.strip())

def run_pipeline(objective: str, 
                 client_instructor: Union[HuggingFaceLLMClient, GPT4AllClient], 
                 client_coder: Union[HuggingFaceLLMClient, GPT4AllClient], 
                 data_gdf: gpd.GeoDataFrame,
                 europe_gdf: gpd.GeoDataFrame, 
                 transform_functions: str, 
                 visualize_functions: str) -> str:
    buffer = io.StringIO()
    data_gdf.info(buf=buffer)
    data_description = buffer.getvalue()
    buffer = io.StringIO()
    europe_gdf.info(buf=buffer)
    europe_gdf_description = buffer.getvalue()
    
    initial_query = QueryProvider.get_query(query_type=QueryType.INITIAL, 
                                            objective=objective, 
                                            data_description=data_description)
    logging.log(logging.INFO, "Running initial query")
    response = client_instructor.query(initial_query)

    logging.log(logging.INFO, f"Initial query finished successfully, response: \n{response}")

    logging.log(logging.INFO, "Started parsing response")
    try:
        parsed_response = extract_json(response)
        transform_instructions = parsed_response["transform"]
        visualize_instructions = parsed_response["visualize"]
        # intermediate_data_description = parsed_response["column_definitions"]
    except Exception as e:
        raise ValueError("Parsed response is not in json format or does not contain transform, visualize, or column_definitions keys.")
    logging.log(logging.INFO, "Parsing successful")

    logging.log(logging.INFO, "Running transform query")
    transform_query = QueryProvider.get_query(query_type=QueryType.TRANSFORM,
                                            objective=transform_instructions,
                                            data_description=data_description,
                                            functions=transform_functions,)
    transform_response = client_coder.query(transform_query)
    
    logging.log(logging.INFO, f"Transform query finished successfully, response: \n{extract_python_code(transform_response)}")
    
    try:
        transform_code = extract_python_code(transform_response)
        cleaned_transform_code = clean_python_code(transform_code)
        description_extraction_function_code = get_description_extraction_function_string(cleaned_transform_code)
        local_scope = {}
        exec(description_extraction_function_code, globals(), local_scope)
        intermediate_data_description = local_scope['get_transformed_data_description'](data_gdf)
    except Exception as e:
        raise ValueError(f"Error while running transform query: {e}")
    
    logging.log(logging.INFO, "Running visualize query")

    visualize_query = QueryProvider.get_query(query_type=QueryType.VISUALIZE,
                                                objective=visualize_instructions,
                                                europe_gdf_description=europe_gdf_description,
                                                intermediate_data_description=intermediate_data_description,
                                                functions=visualize_functions
                                                )

    visualize_response = client_coder.query(visualize_query)
    logging.log(logging.INFO, f"Visualize query finished successfully, response: \n{extract_python_code(visualize_response)}")
    
    try:
        visualize_code = extract_python_code(visualize_response)
        cleaned_visualize_code = clean_python_code(visualize_code)
        solution_function_string = get_solution_function_string(cleaned_transform_code, cleaned_visualize_code)
        local_scope = {}
        exec(solution_function_string, globals(), local_scope)
        local_scope['solve'](data_gdf, europe_gdf)
    except Exception as e:
        raise ValueError(f"Error while running visualize query: {e}")
    
    return solution_function_string