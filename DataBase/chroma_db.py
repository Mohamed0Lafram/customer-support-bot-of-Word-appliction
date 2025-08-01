import chromadb 
import pandas as pd
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Use the free model
#embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient()



#save the document into the chroma database
file = pd.read_json(r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\DataBase\paragraph_chunks.json', lines=True)     
documents = [file.iloc[i,1] for i in range(len(file))]

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    )
# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=documents,
    ids=[f'id{i}' for i in range(len(file))]
)


results = collection.query(
    query_texts=["WHAT IS libreoffice?"], # Chroma will embed this for you
    n_results=4 # how many results to return
)

print(results)
