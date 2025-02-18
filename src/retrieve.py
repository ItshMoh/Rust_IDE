import pandas as pd
import qdrant_client
import psycopg2
from sentence_transformers import SentenceTransformer
import os 
model = SentenceTransformer("all-MiniLM-L6-v2")
from dotenv import load_dotenv
load_dotenv()


qdrant = qdrant_client.QdrantClient(os.getenv('qdr_url'), api_key=os.getenv('qdr_api_key')) 

def search_rust_resources(query):
    query_embedding = model.encode(query).tolist()
    search_results = qdrant.search(collection_name="rust_resources", query_vector=query_embedding, limit=3)

    retrieved_questions = [
        result.payload["indexing_question"] for result in search_results if "indexing_question" in result.payload
    ]
    print(type(retrieved_questions))
    return retrieved_questions

def fetch_from_postgres(questions):
    if not questions:
        return [] 
    conn = psycopg2.connect(
        dbname="rust_rag",
        user=os.getenv('user'),
        password=os.getenv('password'),
        host="127.0.0.1",
        port="5432"
    )
    
    cursor = conn.cursor()
  
    query = "SELECT id, rust_code, summary FROM rust_resources WHERE indexing_question IN %s"
    cursor.execute(query, (tuple(questions),))
    results = cursor.fetchall()  
    conn.close()
    print("type:::",results)
    for result in results:
        print("type of result",type(result[1]))
        print("type of result",type(result[2]))
        print("summary",result[2])
    return results
def retrieve_relevant_docs(prompt):
    retrieved_ids = search_rust_resources(prompt)

    results = fetch_from_postgres(retrieved_ids)

    return results 



