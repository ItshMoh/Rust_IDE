from src.llm_client import QwenCoderClient
# from src.project_generator import ProjectGenerator


def main():
    llm_client = QwenCoderClient()
    prompt = input("Enter your project description: ")
    try:
        
        response = llm_client.generate(prompt)
        print(response)
        
            
    except Exception as e:
        print(f"Error during project generation: {e}")

if __name__ == "__main__":
    main()