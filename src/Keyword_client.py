# import openai
import pandas as pd
import time
import os
import requests
from typing import Dict
import json 
from dotenv import load_dotenv
# from src.project_generator import ProjectGenerator
load_dotenv()

class SummaryKeywordClient:
    def __init__(self,summary):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1-distill-llama-70b"
        self.api_key = os.getenv('API_KEY')
        self.summary = summary

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            
            "Authorization": f"Bearer {self.api_key}"
        }
    
 
    def generate(self):
        endpoint = f"{self.base_url}"
        messages= [
           {
    "role": "system",
    "content": """Given the following summary of a Rust code snippet:
    
    Summary: "{self.summary}"
    
    1. Create a short and precise question that someone might ask to find this Rust resource.
    2. Extract 3-5 important keywords from the summary.
    
    Format the response as:
    
    Indexing Question: <Your Generated Question>
    Keywords: <comma-separated keywords>
     """
}

    ]
        payload = json.dumps({
    "model": "deepseek/deepseek-r1-distill-llama-70b",
    "messages": messages})
        try: 

            response = requests.post(endpoint, headers=self._prepare_headers(), data=payload) 
            print("response json ::",response.json())
            response = response.json()
            result = response["choices"][0]["message"]["content"]
            print("result",result)    
            lines = result.split("\n")
            indexing_question = lines[0].replace("Indexing Question: ", "").strip()
            keywords = lines[1].replace("Keywords: ", "").strip()
            print("index_question",indexing_question)
            print("keywords",keywords)
            return indexing_question, keywords

        except Exception as e:
            print(f"Error processing summary: {self.summary[:50]}... -> {e}")
            return "", ""
       