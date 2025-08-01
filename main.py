from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src import core  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    query: str

@app.post("/message")
def answer_question(question: QuestionRequest):
    # Step 1: Refine the query
    refined_query = core.refined_query(question.query)
    print(f"Refined Query: {refined_query}")

    # Step 2: Join LLM responses
    joined_response = core.join_resonces(refined_query)
    print(f"Joined Response: {joined_response}")

    # Step 3: Vector search
    search_results = core.search_vector_base(joined_response)
    print(f"Search Results: {search_results}")

    # Step 4: Final LLM output
    final_response = core.llm_responce2(refined_query, search_results)

    return {"response": final_response}
