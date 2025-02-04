
import requests
from typing import Dict
import json 
from dotenv import load_dotenv
from src.project_generator import ProjectGenerator
load_dotenv()
import os
class QwenCoderClient:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1-distill-llama-70b"
        self.api_key = os.getenv('API_KEY')

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            
            "Authorization": f"Bearer {self.api_key}"
        }
    
 
    def generate(self,input:str,context:list[dict]) -> dict[str,str]:
        endpoint = f"{self.base_url}"
        messages= [
           {
    "role": "system",
    "content": """You are a Rust development expert. When asked to create a Rust project, you will generate all necessary files for a complete, compilable cargo project. You will be given context that includes your previous responses and errors from the Rust compiler for previous code submissions. Do not provide any explanations—only return code.
    
    Always generate these files:
    1. Cargo.toml with proper metadata and dependencies
    2. src/main.rs or src/lib.rs as appropriate
    3. Any needed module files under src/
    
    Format your response strictly as follows:
    
    [FILE: Cargo.toml]
    ```
    <content>
    ```
    [END FILE]
    
    [FILE: src/main.rs]
    ```
    <content>
    ```
    [END FILE]
    
    [FILE: src/<module_name>.rs]
    ```
    <content>
    ```
    [END FILE]
    
    After every file content block, you must write [END FILE].
    Any additional text outside these structured blocks will be stored in src/README.md.
    
    Ensure all files follow Rust best practices and contain proper module declarations, use statements, and error handling.
    
    If the user asks for a specific file, generate only that file. If the user asks for multiple files, generate them all. If the user requests frontend code, also generate frontend files as specified.
    """
}

    ]
        for entry in context:
       
            print('entry',entry)
            if entry["prompt"]:
                messages.append({"role": "user", "content": entry["prompt"]})
            
           
            if entry["response"] or entry["error"]:
                content = ""
                if entry["response"]:
                    content += entry["response"]
                if entry["error"]:
                    content += f"\nError encountered: {entry['error']}\n"
                    content += "Please consider this error while providing the next solution."
                messages.append({"role": "assistant", "content": content})
        
    
        messages.append({"role": "user", "content": input})
        payload = json.dumps({
    "model": "deepseek/deepseek-r1-distill-llama-70b",
    "messages": messages
    
})
        
        
        response = requests.post(endpoint, headers=self._prepare_headers(), data=payload)
        if response.status_code == 200:
            response_json = response.json()
            print('response_json', response_json)
            if "choices" in response_json and len(response_json["choices"]) > 0:
                response_text = response_json["choices"][0]["message"]["content"]
                # print("Response Text:\n", response_text)
                parsed_files = ProjectGenerator.parse_llm_response(response_text)
                print("Parsed Files:\n", parsed_files)
                project_directory = "generated_rust_project"
                ProjectGenerator.save_files(parsed_files, project_directory)
                # return response_text
                return parsed_files
            else:
                print("Error: No valid response content from the API.")
        else:
            print(f"API Error: {response.status_code}, {response.text}")
       