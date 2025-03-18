import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import time
import pinecone  # Add this import for Pinecone

def convertExcelToVDB():
    pass  # Add this placeholder statement until you implement the function

    start_time = time.time()
    
    #Load Excel file
    file_path = "./data.xlsx"
    df = pd.read_excel(file_path)

    #Select relevant columns to be converted
    columns_to_embed = df.columns

    #Concatenate the values into a single string
    df["combined_text"] = df[columns_to_embed].astype(str).apply(lambda x: " | ".join(x), axis=1)

    #Load a sentence embedding model
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    #Generate embeddings for each row
    embeddings = model.encode(df["combined_text"].tolist())
    
    embeddings = np.array(embeddings).astype('float32')

    # Initialize Pinecone
    pinecone.init(api_key='YOUR_API_KEY', environment='YOUR_ENVIRONMENT')  # Replace with your Pinecone API key and environment
    index_name = "your_index_name"  # Specify your index name
    dimension = embeddings.shape[1]
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension)  # Create index if it doesn't exist
    index = pinecone.Index(index_name)  # Connect to the index

    # Add embeddings to Pinecone
    index.upsert(vectors=[(str(i), embedding) for i, embedding in enumerate(embeddings)])  # Upsert embeddings

    print(f"Stored {len(embeddings)} embeddings in Pinecone.")

    # Searching Example 
    # query_text = "Signs and Barrier issue in Raleigh"
    # query_embedding = model.encode([query_text]).astype('float32')

    # top_k = 5
    # results = index.query(query_embedding.tolist(), top_k=top_k)  # Update to use Pinecone query

    # print("Nearest neighbours indices:", [match.id for match in results.matches])
    # print("Distances: ", [match.score for match in results.matches])

    # Display the retrieved records
    # print("\n ** Top Similar Observations: **\n")
    # for i, match in enumerate(results.matches):
    #     print(f"Rank {i+1}: {df.iloc[int(match.id)].to_dict()}")
    #     print(f"Distance Score: {match.score}\n")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time Taken: {elapsed_time}")

    return {"index":index, "df": df}

# if __name__ == "__main__": 
#     convertExcelToVDB()