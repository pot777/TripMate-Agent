from pydantic import BaseModel
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
    days: int
    budget: int
    schedule: List[ScheduleItem]
    food: List[str]
    budget_breakdown: BudgetBreakdown