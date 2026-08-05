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

@app.get("/chat")
def chat(message: str,session_id: str = "default"):

    answer = run_agent(message,session_id)

    return {
        "user": message,
        "answer": answer.model_dump() if hasattr(answer,"model_dump") else answer
    }