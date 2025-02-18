from src.llm_client import QwenCoderClient
from pymongo import MongoClient
from src.rust_compiler import RustCompiler
from src.summarizer import Summarizer
from src.summarizer import open_text_files
import os
from src.retrieve import retrieve_relevant_docs
client = MongoClient(os.getenv('MONGO_URI'))
db = client['Rust_IDE']
collection = db['Chat-context']

collection.insert_one({"username":"Itshmoh" ,"context":[{"prompt":"", "response": "", "error": ""}]}) #Enter the username
def main():
    llm_client = QwenCoderClient()
    compiler = RustCompiler()
    summarizer = Summarizer()
    prompt = input("Enter your project description: ")
    # knowledge_base = retrieve_relevant_docs(prompt)
    knowledge_base = {}
    status = False
    user_context = open_text_files('/home/kayden/Desktop/rust_project/LFX_wasmedge/IDE/src/database/rust_mongo.txt')
    user_context = summarizer.generate_summary(user_context)
    try:
        while(status!=True):
            doc = collection.find_one({"username":"Itshmoh"}) #Enter the same username that you typed above.
            context = doc["context"]
            
            response = llm_client.generate(prompt,context,knowledge_base,user_context)
            status , error = compiler.compile_project('generated_rust_project/')
            collection.find_one_and_update({"username":"Itshmoh"}, {"$push": {"context": {"prompt": prompt, "response": str(response), "error": error}}}, upsert=True) 
            print("response::",response)
      
    except Exception as e:
        print(f"Error during project generation: {e}")

if __name__ == "__main__":
    main()