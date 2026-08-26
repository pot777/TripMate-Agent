import ast
import json
import re

from ..db.database import SessionLocal
from ..db.models import Conversation, Message, TravelStateRecord, utc_now


def _get_or_create_conversation(db, session_id):
    conversation = db.query(Conversation).get(session_id)

    if conversation is None:
        conversation = Conversation(id=session_id)
        db.add(conversation)
        db.flush()

    return conversation


def _serialize_content(content):
    if isinstance(content, str):
        return content

    if hasattr(content, "model_dump"):
        content = content.model_dump()

    return json.dumps(content, ensure_ascii=False, default=str)


def _deserialize_content(content):
    try:
        return json.loads(content)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        legacy_content = ast.literal_eval(content)
        if isinstance(legacy_content, (dict, list)):
            return legacy_content
    except (ValueError, SyntaxError, TypeError):
        pass

    return content


def _title_from_message(message):
    destination_match = re.search(
        r"(?:去|到)([\u4e00-\u9fa5]{2,8}?)(?:玩|旅游|旅行|游|待|住)",
        message
    )
    days_match = re.search(r"(\d+)\s*(?:天|日)", message)

    if destination_match:
        destination = destination_match.group(1)
        days = days_match.group(1) if days_match else None
        return f"{destination}{days + '日' if days else ''}旅行"

    compact = re.sub(r"\s+", " ", message).strip()
    return f"{compact[:20]}…" if len(compact) > 20 else compact or "新旅行"


def add_message(session_id, role, content):
    content_text = _serialize_content(content)
    db = SessionLocal()

    try:
        conversation = _get_or_create_conversation(db, session_id)
        conversation.updated_at = utc_now()

        if role == "user":
            conversation.preview = content_text[:500]

            has_user_message = (
                db.query(Message.id)
                .filter(
                    Message.conversation_id == session_id,
                    Message.role == "user"
                )
                .limit(1)
                .first()
            )

            if has_user_message is None:
                conversation.title = _title_from_message(content_text)

        db.add(
            Message(
                conversation_id=session_id,
                role=role,
                content=content_text
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_history(session_id):
    db = SessionLocal()

    try:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == session_id)
            .order_by(Message.created_at, Message.id)
            .all()
        )

        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]
    finally:
        db.close()


def list_conversations():
    db = SessionLocal()

    try:
        conversations = (
            db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

        return [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "preview": conversation.preview
            }
            for conversation in conversations
        ]
    finally:
        db.close()


def get_conversation_detail(session_id):
    db = SessionLocal()

    try:
        conversation = db.query(Conversation).get(session_id)

        if conversation is None:
            return None

        messages = (
            db.query(Message)
            .filter(Message.conversation_id == session_id)
            .order_by(Message.created_at, Message.id)
            .all()
        )
        state_record = db.query(TravelStateRecord).get(session_id)
        travel_state = state_record.state_json if state_record else None

        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "preview": conversation.preview,
            "messages": [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": _deserialize_content(message.content),
                    "created_at": message.created_at.isoformat()
                }
                for message in messages
            ],
            "travel_state": travel_state,
            "current_plan": travel_state.get("current_plan") if travel_state else None
        }
    finally:
        db.close()
