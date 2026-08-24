from pydantic import BaseModel, Field
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


states = {}


def get_state(session_id):

    if session_id not in states:

        states[session_id] = TravelState()

    return states[session_id]


def update_state(session_id, **kwargs):

    state = get_state(session_id)

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

    return state