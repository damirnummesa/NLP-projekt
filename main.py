import pandas as pd
from utils.pipeline import run_pipeline
# from clientConversational import HuggingFaceLLMClient
from utils.llm_api.client import HuggingFaceLLMClient
import os, io

def run():
    data = pd.read_csv("./data/LUCAS-SOIL-2018.csv")
    buffer = io.StringIO()
    data.info(buf=buffer)
    data_description = buffer.getvalue()
    
    objective = "Plot the average ‘OC’ for each land type (LC0_Desc). save it as a png."
    with open('./function_headers/all.txt') as f:
        functions = f.readlines()
        functions = "\n".join(functions)

    with open('./function_headers/transform.txt') as f:
        transform_functions = f.readlines()
        transform_functions = "\n".join(functions)
        
    with open('./function_headers/visualize.txt') as f:
        visualize_functions = f.readlines()
        visualize_functions = "\n".join(functions)

    MODEL_NAME_INSTRUCTOR = "codellama/CodeLlama-7b-Instruct-hf"
    MODEL_NAME_CODER = "codellama/CodeLlama-7b-Instruct-hf"
    
    API_KEY = os.getenv("API_KEY")
    
    client_instructor = HuggingFaceLLMClient(model_name=MODEL_NAME_INSTRUCTOR, use_api=False, api_key=API_KEY, device="gpu")
    client_coder = HuggingFaceLLMClient(model_name=MODEL_NAME_CODER, use_api=False, api_key=API_KEY, device="gpu")
    
    run_pipeline(objective=objective, 
                 client_instructor=client_instructor, 
                 client_coder=client_coder, 
                 data_description=data_description, 
                 functions_transform=transform_functions, 
                 functions_visualize=visualize_functions)
    
if __name__ == "__main__":
    run()