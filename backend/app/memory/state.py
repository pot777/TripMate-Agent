from pydantic import BaseModel


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

        if hasattr(state,key) and value is not None:

            setattr(state,key,value)

    return state