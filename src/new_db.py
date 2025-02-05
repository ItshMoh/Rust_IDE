from Keyword_client import SummaryKeywordClient
import pandas as pd
import time
data = pd.read_csv("/home/kayden/Desktop/rust_project/LFX_wasmedge/IDE/src/new_db.csv")
data["Indexing Question"] = ""
data["Keywords"] = ""

for index, row in data.iterrows():
    summary = row["summary"]
    if pd.notna(summary):
        client = SummaryKeywordClient(summary)
        indexing_question, keywords = client.generate()
        data.at[index, "Indexing Question"] = indexing_question
        data.at[index, "Keywords"] = keywords
        time.sleep(1)  


data.to_csv("rust_resources_updated.csv", index=False)

print("Updated CSV file saved with Indexing Questions and Keywords!")