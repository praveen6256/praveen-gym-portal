from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MembershipHistory(BaseModel):
    id: Optional[str] = None
    user_id: str
    user_name: str
    user_email: str
    action: str  # "activated" | "removed"
    performed_by: str  # admin user_id
    performed_by_name: str
    performed_at: datetime
    notes: Optional[str] = None


class NutritionRequest(BaseModel):
    weight: float
    height: float
    age: int
    gender: str
    activity_level: str
    fitness_goal: str
    dietary_preference: str


class MacroResult(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    water_liters: float
    bmr: float
    tdee: float


class NutritionResponse(BaseModel):
    macros: MacroResult
    disclaimer: str = (
        "These are general fitness estimates based on standard formulas. "
        "They are NOT medical advice. Please consult a qualified nutritionist "
        "or healthcare professional for personalised guidance."
    )
