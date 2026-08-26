from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .agent.runner import run_graph
from .db.database import init_db
from .memory.store import get_conversation_detail, list_conversations
from .memory.state import update_state
from .models import TravelPlan


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TripMate Agent API",
    lifespan=lifespan
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


@app.get("/conversations")
def conversations():
    return list_conversations()


@app.get("/conversations/{conversation_id}")
def conversation_detail(conversation_id: str):
    conversation = get_conversation_detail(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "conversation_not_found",
                "message": "旅行对话不存在"
            }
        )

    return conversation


@app.put("/conversations/{conversation_id}/plan")
def update_conversation_plan(conversation_id: str, plan: TravelPlan):
    if get_conversation_detail(conversation_id) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "conversation_not_found",
                "message": "旅行对话不存在"
            }
        )

    state = update_state(
        conversation_id,
        current_plan=plan.model_dump()
    )

    return {
        "current_plan": state.current_plan
    }
