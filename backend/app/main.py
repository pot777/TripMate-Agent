from fastapi import FastAPI


app = FastAPI(
    title="TripMate Agent API"
)


@app.get("/")
def root():
    return {
        "message": "TripMate Agent Backend Running"
    }