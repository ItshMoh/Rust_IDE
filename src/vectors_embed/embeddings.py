import pandas as pd
import qdrant_client
import psycopg2
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import os 
import numpy as np
from dotenv import load_dotenv
load_dotenv()

df = pd.read_csv("src/database/rust_resources_updated.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = qdrant_client.QdrantClient(os.getenv('qdr_url'), api_key=os.getenv('qdr_api_key')) 
COLLECTION_NAME = "rust_resources"

# try:
#     qdrant.get_collection(COLLECTION_NAME)
# except:
#     qdrant.create_collection(
#         COLLECTION_NAME,
#         vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) 
#     )

pg_conn = psycopg2.connect(
    dbname="rust_rag", user=os.getenv('user'), password=os.getenv('password'), host="localhost", port="5432"
)
pg_cursor = pg_conn.cursor()
pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS rust_resources (
        id SERIAL PRIMARY KEY,
        rust_code TEXT,
        summary TEXT,
        indexing_question TEXT,
        keywords TEXT
    );
""")
pg_conn.commit()

def generate_embedding(text):
    if isinstance(text, float) and np.isnan(text): 
        return []  
    
    text = str(text).strip() 
    
    if not text:  
        return []
    return model.encode(text).tolist()

for index, row in df.iterrows():
    question = row["Indexing Question"]
    keywords = row["Keywords"]
    rust_code = row["original_text"]
    summary = row["summary"]

   
    embedding_vector = generate_embedding(question)

    
    if embedding_vector and isinstance(embedding_vector, list) and len(embedding_vector) > 0:
        qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=index,
                vector=embedding_vector,  
                payload={"indexing_question": question, "keywords": keywords}
            )
        ]
    )
        pg_cursor.execute(
        "INSERT INTO rust_resources (rust_code, summary, indexing_question, keywords) VALUES (%s, %s, %s, %s)",
        (rust_code, summary, question, keywords)
    )
else:
    print(f"Skipping embedding for index {index} due to invalid data.")
    
    pg_cursor.execute(
        "INSERT INTO rust_resources (rust_code, summary, indexing_question, keywords) VALUES (%s, %s, %s, %s)",
        (rust_code, summary, question, keywords)
    )

pg_conn.commit()
pg_cursor.close()
pg_conn.close()

print("Embeddings stored in Qdrant, metadata stored in PostgreSQL!")
