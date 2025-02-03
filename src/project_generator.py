
import os
from typing import Dict

class ProjectGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.cache_dir = "./generated_projects"

    def parse_llm_response(response: str) -> Dict[str, str]:
        """Parses the LLM response, extracts file content inside triple backticks, and stores extra text in README.md."""
        files = {}
        current_file = None
        current_content = []
        extra_text = []
        inside_file = False
        inside_code_block = False
        
        lines = response.split('\n')
        
        for line in lines:
            if line.startswith('[FILE:'):
                if current_file and current_content:
                    files[current_file] = '\n'.join(current_content).strip()
                current_file = line[6:].strip().rstrip(']')
                current_content = []
                inside_file = True
                inside_code_block = False  
            elif line.startswith('[END FILE]'):
                if current_file and current_content:
                    files[current_file] = '\n'.join(current_content).strip()
                current_file = None
                inside_file = False
                inside_code_block = False
            elif inside_file:
                if line.strip().startswith('```'):
                    inside_code_block = not inside_code_block 
                    continue
                if inside_code_block:
                    current_content.append(line)
            else:
                extra_text.append(line)  
        
        if extra_text:
            files["src/README.md"] = '\n'.join(extra_text).strip()
        
        return files

    def save_files(files: Dict[str, str], project_dir: str):
        """Saves extracted files from LLM response to disk."""
        for filepath, content in files.items():
            full_path = os.path.join(project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"Files saved successfully in {project_dir}")
