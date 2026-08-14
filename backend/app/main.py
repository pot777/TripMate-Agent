from fastapi import FastAPI
from .agent.runner import run_graph


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

    answer = run_graph(message, session_id)

    return {
        "user": message,
        "answer": answer.model_dump() if hasattr(answer,"model_dump") else answer
    }