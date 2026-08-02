from fastapi import FastAPI
from .agent import run_agent

app = FastAPI(
    title="TripMate Agent API"
)


@app.get("/")
def root():
    return {
        "message": "TripMate Agent Backend Running"
    }

from app.llm import chat_with_llm

@app.get("/chat")
def chat(message: str):

    answer = run_agent(message)

    return {
        "user": message,
        "answer": answer.model_dump() if hasattr(answer,"model_dump") else answer
    }