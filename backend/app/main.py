from fastapi import FastAPI


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

    answer = chat_with_llm(message)

    return {
        "user": message,
        "answer": answer.model_dump()
    }