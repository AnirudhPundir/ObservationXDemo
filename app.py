import ollama;
import pandas as pd;
from sentence_transformers import SentenceTransformer;
import faiss;
import numpy as np;
from excelToVectorDB import convertExcelToVDB;
import time

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")


def search_faiss(query, index, df, top_k=3):
    #Searching Example 
    query_embedding = model.encode([query]).astype('float32')
    top_k = 5
    D, I = index.search(query_embedding, top_k)

    print("Nearest neighbours indices:", I)
    print("Distances: ", D)

    # Display the retrieved records
    context = []
    for i, idx in enumerate(I[0]):
        if idx < len(df):
            context.append(df.iloc[idx].to_dict())

    return context

def search_faiss_DB(query, top_k=3):
    index = faiss.read_index("observations.index")
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    query_embedding = model.encode([query]).astype('float32')
    distance, indices = index.search(query_embedding, top_k)
    retrieved_context = []
    for idx in indices[0]:
        stored_text = index.reconstruct(int(idx))
        retrieved_context.append(stored_text.decode("utf-8"))
    context = "\n".join(retrieved_context)

    return context


#Example 

# query = "Train my model"
# results = search_faiss(query)

# for q, a, score in results: 
#     print("Similar Question: {q}\n Answer: {a} \n Distance: {score}\n")
# user_input
def chat_with_ollama(user_input):
    print("Chatbot (Deepseek R1) is ready! Type 'exit' to quit ")

    # Retrieve similar knowledge from FAISS
    result = convertExcelToVDB()

    # while(True):
    #     user_input = input("You: ")
    #     if user_input.lower() == "exit" :
    #         print("Chatbot: Goodbye!")
    #         break

    # user_input = "create an observation for oil spill in kitchen"

    context = search_faiss(user_input, result["index"], result["df"])

    start_time = time.time()

    # context = search_faiss_DB(user_input)

    #Create a structured prompt for the model
    prompt = f"""
    You are an AI that generates structured JSON based on retrieved observations.

    ### Context:
    {context}

    ### Instructions:
    - Extract the following fields from the retrieved data and input query:
      - Area
      - Category
      - Company
      - Description
      - Observation Date (YYYY-MM-DD)
      - Observation Type
      - Observer
      - Priority Level (1-5)
      - Project
      - Severity Level (Low, Medium, High, Critical)
      - Site
      - Source
      - Status (Open, In Progress, Resolved, Closed)
    - Ensure missing values are set to `null`.

    ### Input Query:
    {user_input}

    ### **Instructions:**
    - Extract and return only the JSON.
    - Do not provide any explanations, reasoning, or extra text.
    - Ensure correct data types and formatting.

    ### Expected JSON Output:
    ```json
    {{
        "Area": "<string | null>",
        "Category": "<string | null>",
        "Company": "<string | null>",
        "Description": "<string>",
        "Observation Date": "<string | YYYY-MM-DD | null>",
        "Observation Type": "<string | null>",
        "Observer": "<string | null>",
        "Priority Level": "<integer | 1-5 | null>",
        "Project": "<string | null>",
        "Severity Level": "<string | Low, Medium, High, Critical | null>",
        "Site": "<string | null>",
        "Source": "<string | null>",
        "Status": "<string | Open, In Progress, Resolved, Closed | null>"
    }}
    ```
    """

    response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt}])

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time Taken: {elapsed_time}")

    print(1)

    print({"Response": response["message"]["content"]})

    return response

# if __name__ == "__main__":
#     chat_with_ollama()