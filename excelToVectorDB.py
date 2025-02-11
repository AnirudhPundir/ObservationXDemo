import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import time

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

    #Create a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    #Save the FAISS index
    faiss.write_index(index, "observations.index")

    print(f"Stored {len(embeddings)} embeddings in FAISS.")


    #Searching Example 
    # query_text = "Signs and Barrier issue in Raleigh"
    # query_embedding = model.encode([query_text]).astype('float32')

    # top_k = 5
    # D, I = index.search(query_embedding, top_k)

    # print("Nearest neighbours indices:", I)
    # print("Distances: ", D)

    # Display the retrieved records
    # print("\n ** Top Similar Obeservations: **\n")
    # for i, idx in enumerate(I[0]):
    #     if idx < len(df):
    #         print(f"Rank {i+1}: {df.iloc[idx].to_dict()}")
    #         print(f"Distance Score: {D[0][i]}\n")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time Taken: {elapsed_time}")

    return {"index":index, "df": df}

# if __name__ == "__main__": 
#     convertExcelToVDB()