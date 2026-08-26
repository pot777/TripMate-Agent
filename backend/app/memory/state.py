from pydantic import BaseModel, Field

from ..db.database import SessionLocal
from ..db.models import Conversation, TravelStateRecord, utc_now
from ..utils.date_parser import normalize_date


class TravelState(BaseModel):

    destination: str | None = None

    days: int | None = None

    budget: int | None = None

    start_date: str | None = None

    weather: dict = Field(default_factory=dict)

    travel_knowledge: list[str] = Field(default_factory=list)

    current_plan: dict | None = None

    travelers: list[str] = Field(default_factory=list)

    preferences: list[str] = Field(default_factory=list)

    interests: list[str] = Field(default_factory=list)


def _get_or_create_records(db, session_id):
    conversation = db.query(Conversation).get(session_id)

    if conversation is None:
        conversation = Conversation(id=session_id)
        db.add(conversation)
        db.flush()

    state_record = db.query(TravelStateRecord).get(session_id)

    if state_record is None:
        state = TravelState()
        state_record = TravelStateRecord(
            conversation_id=session_id,
            state_json=state.model_dump()
        )
        db.add(state_record)
        db.flush()
    else:
        state = TravelState.model_validate(state_record.state_json)

    return conversation, state_record, state


def get_state(session_id):
    db = SessionLocal()

    try:
        _, _, state = _get_or_create_records(db, session_id)
        db.commit()
        return state
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def update_state(session_id, **kwargs):
    db = SessionLocal()

    try:
        conversation, state_record, state = _get_or_create_records(db, session_id)

        for key, value in kwargs.items():

            if key == "start_date" and value:
                value = normalize_date(value)

            if not hasattr(state, key) or value is None:
                continue

            if key in ["travelers", "preferences", "interests"]:

                current_value = getattr(state, key)

                merged_value = list(
                    dict.fromkeys(
                        current_value + value
                    )
                )

                setattr(
                    state,
                    key,
                    merged_value
                )

            else:

                setattr(
                    state,
                    key,
                    value
                )

        now = utc_now()
        state_record.state_json = state.model_dump()
        state_record.updated_at = now
        conversation.updated_at = now

        if state.current_plan:
            destination = state.current_plan.get("destination") or state.destination
            days = state.current_plan.get("days") or state.days

            if destination:
                conversation.title = f"{destination}{str(days) + '日' if days else ''}游"

        db.commit()
        return state
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
