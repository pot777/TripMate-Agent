from pydantic import BaseModel
from ..utils.date_parser import normalize_date

class TravelState(BaseModel):

    destination: str | None = None

    days: int | None = None

    budget: int | None = None

    start_date: str | None = None

    weather: dict | None = None


states = {}


def get_state(session_id):

    if session_id not in states:

        states[session_id] = TravelState()

    return states[session_id]


def update_state(session_id, **kwargs):

    state = get_state(session_id)

    for key,value in kwargs.items():

        if key == "start_date" and value:
            value = normalize_date(value)

        if hasattr(state,key) and value is not None:
            setattr(state,key,value)

    return state