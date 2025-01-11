from client import HuggingFaceLLMClient
from query import QueryProvider, QueryType
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def run_pipeline(objective: str, 
                 client_instructor: HuggingFaceLLMClient, 
                 client_coder: HuggingFaceLLMClient, 
                 data_description: str, 
                 functions_transform: str, 
                 functions_visualize: str):
    
    initial_query = QueryProvider.get_query(query_type=QueryType.INITIAL, 
                                            objective=objective, 
                                            data_description=data_description)
    logging.log(logging.INFO, "Running initial query")
    response = client_instructor.query(initial_query)
    
    logging.log(logging.INFO, f"Initial query finished successfully, response: {response}")

    logging.log(logging.INFO, "Started parsing response")
    try:
        parsed_response = json.loads(response)
        transform_instructions = parsed_response["transform"]
        visualize_instructions = parsed_response["visualize"]
        intermediate_data_description = parsed_response["column_definitions"]
    except Exception as e:
        raise ValueError("Parsed response is not in json format or does not contain transform, visualize, or column_definitions keys.")
    logging.log(logging.INFO, "Parsing successful")

    logging.log(logging.INFO, "Running transform query")
    transform_query = QueryProvider.get_query(query_type=QueryType.TRANSFORM,
                                            objective=transform_instructions,
                                            data_description=data_description,
                                            functions=functions_transform,
                                            intermediate_data_description=intermediate_data_description)
    transform_response = client_coder.query(transform_query)

    logging.log(logging.INFO, f"Transform query finished successfully, response: {extract_python_code(transform_response)}")
    
    logging.log(logging.INFO, "Running visualize query")

    visualize_query = QueryProvider.get_query(query_type=QueryType.VISUALIZE,
                                              objective=visualize_instructions,
                                              intermediate_data_description=intermediate_data_description,
                                              functions=functions_visualize
                                              )

    visualize_response = client_coder.query(visualize_query)
    logging.log(logging.INFO, f"Visualize query finished successfully, response: {extract_python_code(visualize_response)}")
    
    
def extract_python_code(response: str) -> str:
    response = response.split("```python")
    if len(response) > 1:
        response = response[1].split("```")
        return response[0].strip()
    return response.strip()