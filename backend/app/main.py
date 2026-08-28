from contextlib import asynccontextmanager
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from .agent.runner import run_graph, run_graph_stream
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

    answer, trace = run_graph(message, session_id, include_trace=True)

    return {
        "user": message,
        "answer": answer.model_dump() if hasattr(answer,"model_dump") else answer,
        "trace": trace
    }


@app.get("/chat/stream")
def chat_stream(message: str, session_id: str = "default"):
    def event_stream():
        try:
            for item in run_graph_stream(message, session_id):
                payload = json.dumps(item["data"], ensure_ascii=False)
                event_name = item["data"].get("name", item["event"])
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] yield {event_name}", flush=True)
                yield f"event: {item['event']}\ndata: {payload}\n\n"
        except Exception:
            payload = json.dumps(
                {
                    "type": "error",
                    "message": "旅行规划失败，请稍后重试"
                },
                ensure_ascii=False
            )
            yield f"event: error\ndata: {payload}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


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
