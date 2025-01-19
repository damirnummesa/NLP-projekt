from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import requests
from pydantic import BaseModel
from typing import Optional, Union

class GPT4AllMessage(BaseModel):
    content: str
    role: str

class GPT4AllRequest(BaseModel):
    model: str
    messages: list[GPT4AllMessage]
    max_tokens: int
    temperature: float
    
class Choice(BaseModel):
    finish_reason: str
    index: int
    logprobs: Optional[Union[dict, None]]
    message: GPT4AllMessage
    references: Optional[Union[dict, None]]

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    choices: list[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage

class GPT4AllClient:
    
    def __init__(self, base_url: str = 'http://localhost:4891/v1', model_name: str = None):
        super().__init__()
        self.base_url = base_url
        self.chosen_model = model_name
        
    def get_available_models(self) -> list[str]:
        """Get the list of available models from the GTP4All server"""
        available_model_ids = []
        
        try: 
            response = requests.get(f'{self.base_url}/models')
            response.raise_for_status()
            available_models_response =  response.json()
            
            for model_info in available_models_response['data']:
                available_model_ids.append(model_info['id'])
        except Exception as e:
            print(f'Encountered error while getting available models: {e}')
            
        return available_model_ids
    
    def query(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> Optional[str]:
        """Fetch chat completion response of the specified model for the given message and execution parameters"""
        try:
            message = GPT4AllMessage(content=prompt, role='user')
            request_body = GPT4AllRequest(
                model=self.chosen_model, 
                messages=[message.model_dump()], 
                max_tokens=max_tokens, 
                temperature=temperature,
            )
            response = requests.post(
                url=f'{self.base_url}/chat/completions', 
                json=request_body.model_dump(),
            )
            response.raise_for_status()
            chat_completion_resp = ChatCompletionResponse(**response.json())
            
            return chat_completion_resp.choices[0].message.content
        except Exception as e:
            print(f'Encountered error while generating chat completion: {e}')
            
        return None

class HuggingFaceLLMClient:

    def __init__(self, model_name: str, use_api: bool = False, api_key: str = "", device: str = "cpu"):
        
        self.use_api = use_api
        self.model_name = model_name
        if use_api:
            if not api_key:
                raise ValueError("Please provide an API key to use the Hugging Face API.")
            self.api_key = api_key
            self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            self.headers = {"Authorization": f"Bearer {api_key}"}

        else:
            self.device = 0 if torch.cuda.is_available() and device == "cuda" else -1
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=api_key)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, token=api_key, torch_dtype=torch.float16)
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)

    def query(self, prompt: str, temperature: float = 0.7) -> str:

        if self.use_api:
            return self._query_api(prompt, temperature)
        else:
            return self._query_local(prompt, temperature)
        
    def _query_api(self, prompt: str, temperature: float) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 4096,
                "temperature": temperature,
                "return_full_text": False
                }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"An error occurred with the API: {response.json()}")
            return response.json()[0]["generated_text"].strip()
        except Exception as e:
            return f"An error occurred with the API: {e}"

    def _query_local(self, prompt: str, temperature: float) -> str:
        try:
            response = self.generator(
                prompt,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return response
        except Exception as e:
            return f"An error occurred while trying to run inference: {e.with_traceback()}"
