# models.py
from pydantic import BaseModel,Field
from typing import List


class ScheduleItem(BaseModel):
    day: int
    title: str
    activities: List[str]
    transportation: str
    accommodation_suggestion: str


class BudgetBreakdown(BaseModel):
    transportation: int
    accommodation: int
    food: int
    entertainment: int
    misc: int
    total_estimated: int


class TravelPlan(BaseModel):
    destination: str
    days: int = Field(
        gt=0,
        description="旅行天数，必须大于0"
    )
    budget: int = Field(
        gt=0,
        description="旅行预算，必须大于0"
    )
    schedule: List[ScheduleItem]
    food: List[str]
    budget_breakdown: BudgetBreakdown


from typing import Literal

class AgentAction(BaseModel):
    action: Literal[
        "tool",
        "need_information",
        "direct_answer",
        "generate_plan",
        "modify_plan"
    ]
    tool: str | None = None
    arguments: dict = {}
    answer: str | None = None
    message: str | None = None