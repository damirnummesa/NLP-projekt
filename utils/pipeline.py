from utils.extraction import clean_python_code, extract_python_code, get_description_extraction_function_string, get_solution_function_string
from utils.llm_api.client import HuggingFaceLLMClient, GPT4AllClient
from utils.llm_api.query import QueryProvider, QueryType
import json
import logging
from typing import Callable, Union
import re
import io
import geopandas as gpd

## needed for running solution
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
import matplotlib as mpl
import seaborn as sns
import scipy
import sklearn
import numpy as np
from sklearn.cluster import KMeans
import sklearn as sk
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def run_pipeline(objective: str, 
                 client_instructor: Union[HuggingFaceLLMClient, GPT4AllClient], 
                 client_coder: Union[HuggingFaceLLMClient, GPT4AllClient], 
                 data_gdf: gpd.GeoDataFrame,
                 data_gdf_description: str,
                 europe_gdf: gpd.GeoDataFrame,
                 europe_gdf_description: str,
                 retry_count: int) -> str:
    
    # Transform part
    error = None
    error_code = None
    for _ in range(retry_count):
        query_type = QueryType.TRANSFORM if error is None else QueryType.TRANSFORM_ERROR
        transform_query = QueryProvider.get_query(query_type=query_type, 
                                                  objective=objective, 
                                                  data_gdf_description=data_gdf_description,
                                                  error=error,
                                                  error_code=error_code)
        response = client_instructor.query(transform_query)
        logging.log(logging.INFO, f"Query finished successfully, response: \n{response}")
        transform_code = None
        try:
            transform_code = extract_python_code(response)
            cleaned_transform_code = clean_python_code(transform_code)
            description_extraction_function_code = get_description_extraction_function_string(cleaned_transform_code)
            local_scope = {}
            exec(description_extraction_function_code, globals(), local_scope)
            intermediate_data_description = local_scope['get_transformed_data_description'](data_gdf)
            error = None
            error_code = None
            break
        except Exception as e:
            logging.log(logging.INFO, f"Error while running transform query: {e}")
            error = e
            error_code = transform_code
    if error is not None:
        raise ValueError(f"Error while running transform query: {error}")
    
    
    # Visualize part
    for _ in range(retry_count):
        type_query = QueryProvider.get_query(query_type=QueryType.TYPE, objective=objective)
        response = client_coder.query(type_query)
        logging.log(logging.INFO, f"Query finished successfully, response: \n{response}")
        if response.strip().lower() in ["print", "graph", "map"]:
            break
        
    visualize_query_type, visualize_error_query_type = resolve_visualize_query(response)
    error = None
    error_code = None
    
    for _ in range(retry_count):
        query_type = visualize_query_type if error is None else visualize_error_query_type
        visualize_query = QueryProvider.get_query(query_type=query_type,
                                                  objective=objective,
                                                  europe_gdf_description=europe_gdf_description,
                                                  intermediate_data_description=intermediate_data_description,
                                                  error=error,
                                                  error_code=error_code)
        response = client_coder.query(visualize_query)
        logging.log(logging.INFO, f"Query finished successfully, response: \n{response}")
        visualize_code = None
        try:
            visualize_code = extract_python_code(response)
            cleaned_visualize_code = clean_python_code(visualize_code)
            solution_function_string = get_solution_function_string(cleaned_transform_code, cleaned_visualize_code)
            local_scope = {}
            exec(solution_function_string, globals(), local_scope)
            local_scope['solve'](data_gdf, europe_gdf)
            error = None
            error_code = None
            break
        except Exception as e:
            logging.log(logging.INFO, f"Error while running visualize query: {e}")
            error = e
            error_code = visualize_code
    if error is not None:
        raise ValueError(f"Error while running visualize query: {error}")
    return solution_function_string


def resolve_visualize_query(visualize_type):
    visualize_type = visualize_type.strip().lower()
    if visualize_type in "map":
        return (QueryType.VISUALIZE_MAP, QueryType.VISUALIZE_MAP_ERROR)
    elif visualize_type in "graph":
        return (QueryType.VISUALIZE_GRAPH, QueryType.VISUALIZE_GRAPH_ERROR)
    elif visualize_type in "print":
        return (QueryType.VISUALIZE_PRINT, QueryType.VISUALIZE_PRINT_ERROR)
    else:
        raise ValueError("Visualize type not recognized.")