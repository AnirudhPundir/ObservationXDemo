def read_data_from_excel(): 
    df = pd.read_excel("data.xlsx")
    df = df.dropna() # Remove empty rows if any

    documents = df["question"].toList()
    answers = df["answer"].toList()

    return {"documents": documents, "answers": answers}


data = read_data_from_excel()
documents = data["documents"]
answers = data["answers"]


def generate_embeddings():
    #Load a pre trained model

    # data = read_data_from_excel()
    # documents = data["documents"]
    # answers = data["answers"]

    #Generate embeddings for all questions
    questions_embeddings = model.encode(documents, normalize_embeddings=True)

    return {questions_embeddings}

def store_in_VDB():
    #Define the dimension of embeddings
    embeddings = generate_embeddings()

    embeddings_dim = embeddings.shape[1]

    #Create a FAISS index
    index = faiss.IndexFlat12(embeddings_dim)
    index.add(np.array(embeddings))

    # Save it in DB
    # faiss.write_index(index, "faiss_index.bin")

    return index

    #Resuse 
    #index = faiss.read_index("faiss_index.bin")
s