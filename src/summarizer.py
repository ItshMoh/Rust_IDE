import requests
import json 
import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv()
def open_text_files(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
      text = file.read()
    return text  



class Summarizer:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1-distill-llama-70b"
        self.api_key = os.getenv('API_KEY')
 
    def _prepare_headers(self) -> Dict[str, str]:
        return {
            
            "Authorization": f"Bearer {self.api_key}"
        } 
    def generate_summary(self,input: str) :
            endpoint = f"{self.base_url}"
            messages= [
            {
        "role": "system",
        "content": """You are an advanced AI assistant that summarizes text while retaining all code blocks exactly as written. Given a text input, your task is to generate a concise yet informative summary that preserves the meaning and context of the original content.

Instructions:
1. Retain all code blocks as they appear in the input, ensuring no modifications to indentation, spacing, or syntax. Wrap them in triple backticks (```).
2. Summarize the textual content by extracting key ideas, removing redundancy, and keeping only the most relevant points.
3. Ensure that the summary is structured, clear, and useful as context for another AI model.
4. If the text contains multiple sections, mention key topics covered but avoid unnecessary detail.
5. The final output should be concise while ensuring the essential information is intact.

        """
    }
        ]   
            messages.append({"role": "user", "content": input})
            payload = json.dumps({
        "model": "deepseek/deepseek-r1-distill-llama-70b",
        "messages": messages
        
    })
            response = requests.post(endpoint, headers=self._prepare_headers(), data=payload)
            if response.status_code == 200:
                response_json = response.json()
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    response_text = response_json["choices"][0]["message"]["content"]
                    return response_text
                else:
                    print("Error: No valid response content from the API.")
            else:
                print(f"API Error: {response.status_code}, {response.text}")

       