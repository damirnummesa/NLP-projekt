import pandas as pd
from pipeline import run_pipeline
# from clientConversational import HuggingFaceLLMClient
from client import HuggingFaceLLMClient
import os, io

def run():
    data = pd.read_csv("./data/LUCAS-SOIL-2018.csv")
    buffer = io.StringIO()
    data.info(buf=buffer)
    data_description = buffer.getvalue()
    
    objective = "Plot the average ‘OC’ for each land type (LC0_Desc). save it as a png."
    with open('./action_headers.txt') as f:
        functions = f.readlines()
        functions = "\n".join(functions)

    MODEL_NAME_INSTRUCTOR = "meta-llama/Meta-Llama-3-8B-Instruct"
    MODEL_NAME_CODER = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    API_KEY = os.getenv("API_KEY")
    
    client_instructor = HuggingFaceLLMClient(model_name=MODEL_NAME_INSTRUCTOR, use_api=True, api_key=API_KEY, device="gpu")
    client_coder = HuggingFaceLLMClient(model_name=MODEL_NAME_CODER, use_api=True, api_key=API_KEY, device="gpu")
    
    run_pipeline(objective=objective, 
                 client_instructor=client_instructor, 
                 client_coder=client_coder, 
                 data_description=data_description, 
                 functions_transform=functions, 
                 functions_visualize=functions)
    
if __name__ == "__main__":
    run()