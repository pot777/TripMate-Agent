from fastapi import FastAPI


app = FastAPI(
    title="TripMate Agent API"
)


@app.get("/")
def root():
    return {
        "message": "TripMate Agent Backend Running"
    }

@app.get("/chat")
def chat(message: str):
    return {
        "user": message,
        "answer": "这里以后接入大语言模型"
    }