
import os
from typing import Dict

class ProjectGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.cache_dir = "./generated_projects"

    def parse_llm_response(response: str) -> Dict[str, str]:
        """Parses the LLM response and extracts file content while removing triple backticks and file type indicators."""
        files = {}
        current_file = None
        current_content = []
        inside_file = False  

        for line in response.split('\n'):
            if line.startswith('[FILE:'):
                if current_file: 
                    files[current_file] = '\n'.join(current_content).strip()
                current_file = line[6:].strip().rstrip(']')
                current_content = []
                inside_file = True  
            elif line.startswith('[END FILE]'):
                if current_file:
                    files[current_file] = '\n'.join(current_content).strip()
                    current_file = None  
                inside_file = False
            elif inside_file:
                if line.strip().startswith('```'):
                    continue
                current_content.append(line)

        return files  
    def save_files(files: Dict[str, str], project_dir: str):
        """Saves extracted files from LLM response to disk."""
        for filepath, content in files.items():
            full_path = os.path.join(project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        print(f"Files saved successfully in {project_dir}") 