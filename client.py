from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import requests


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
