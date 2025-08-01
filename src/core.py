from google import genai
import chromadb
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# Access the keys
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# Initialize the Google GenAI client
client = genai.Client(api_key=api_key)

# Initialize the ChromaDB client
chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection("my_collection")



def refined_query(query):
    #get the query from the user and refined it 
    prompt = f'Refine the following query: "{query}" to be more specific and clear. in you awnser only give me the refined query without any additional text. do not write anything except the refined version of the query.'

    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
    )
    return response.text


def llm_response1(query):
    #get the response from the llm
    
    instruction = "Answer this question in one paragraph and do not use any additional text,question : "
    prompt = f'{instruction}{query}'


    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    ll_respoce1 = response.text
    return ll_respoce1


def join_resonces(query):
    response1 = llm_response1(query)
    return f'{response1} {query}'


def search_vector_base(query):
    global collection

    # Search the vector database
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results["documents"][0] if results["documents"] else None


def llm_responce2(refined_query,search_results):
    # Get the response from the LLM using the refined query
    prompt = f'Answer the following question question : {refined_query } .based on the provided context: "{search_results}"'

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    return response.text
