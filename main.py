from src.llm_client import QwenCoderClient
from src.project_generator import ProjectGenerator
from pymongo import MongoClient
from src.rust_compiler import RustCompiler
import os
client = MongoClient(os.getenv('MONGO_URI'))
db = client['Rust_IDE']
collection = db['Chat-context']
# here in the place of username enter a name and it will make a user.
collection.insert_one({"username":"Itshmoh" ,"context":[{"prompt":"", "response": "", "error": ""}]})
def main():
    llm_client = QwenCoderClient()
    compiler = RustCompiler()
    prompt = input("Enter your project description: ")
    status = False
    try:
        while(status!=True):
            doc = collection.find_one({"username":"Itshmoh"}) #Enter the same username that you typed above.
            context = doc["context"]
            response = llm_client.generate(prompt,context)
            status , error = compiler.compile_project('generated_rust_project/')
            collection.find_one_and_update({"username":"Itshmoh"}, {"$push": {"context": {"prompt": prompt, "response": response, "error": error}}}, upsert=True) 
            print(response)
      
    except Exception as e:
        print(f"Error during project generation: {e}")

if __name__ == "__main__":
    main()