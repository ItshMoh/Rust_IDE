
import requests
from typing import Dict
import json
import backoff  
from dotenv import load_dotenv
from src.project_generator import ProjectGenerator
load_dotenv()
import os
class QwenCoderClient:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "qwen-2.5-coder-7b"
        self.api_key = os.getenv('API_KEY')

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    @backoff.on_exception(backoff.expo, 
                         (requests.exceptions.Timeout, 
                          requests.exceptions.ConnectionError),
                         max_tries=3)
    def generate(self,input:str) -> str:
        endpoint = f"{self.base_url}"
        
        payload = json.dumps({
    "model": "qwen/qwen-2.5-7b-instruct",
    "messages": [
        {"role": "system", "content": """You are a Rust development expert. When asked to create a Rust project, you will generate all necessary files for a complete, compilable cargo project. 

Always generate these files:
1. Cargo.toml with proper metadata and dependencies
2. src/main.rs or src/lib.rs as appropriate
3. Any needed module files under src/

Format your response like this:

[FILE: Cargo.toml]
<content>
[END FILE]

[FILE: src/main.rs]
<content>
[END FILE]

[FILE: src/<module_name>.rs]
<content>
[END FILE]

Ensure all files follow Rust best practices and contain proper module declarations, use statements, and error handling.
If the user asks for a specific file, only generate that file. If the user asks for multiple files, generate them all. 
If the user asks to generate frontend, also generate frontend for the project as the user suggests.
"""},
        {"role": "user", "content": input} 
    ]
})
        
        
        response = requests.post(endpoint,headers= self._prepare_headers(),data=payload )
        if response.status_code == 200:
            response_json = response.json()
            print('response_json', response_json)
            if "choices" in response_json and len(response_json["choices"]) > 0:
                response_text = response_json["choices"][0]["message"]["content"]
    
                parsed_files = ProjectGenerator.parse_llm_response(response_text)
                print("Parsed Files:\n", parsed_files)
                project_directory = "generated_rust_project"
                ProjectGenerator.save_files(parsed_files, project_directory)
            else:
                print("Error: No valid response content from the API.")
        else:
            print(f"API Error: {response.status_code}, {response.text}")
       