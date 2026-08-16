from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class FitnessGoal(str, Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    maintain = "maintain"
    endurance = "endurance"


class DietaryPreference(str, Enum):
    vegetarian = "vegetarian"
    non_vegetarian = "non_vegetarian"
    vegan = "vegan"


class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"


class Role(str, Enum):
    member = "member"
    admin = "admin"


class MembershipType(str, Enum):
    standard = "standard"
    premium = "premium"


# --- Request Models ---

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    gender: Gender
    age: int = Field(..., ge=10, le=100)
    height: float = Field(..., gt=50, le=300, description="Height in cm")
    weight: float = Field(..., gt=20, le=500, description="Weight in kg")
    phone: str = Field(..., min_length=7, max_length=20)
    fitness_goal: FitnessGoal
    dietary_preference: DietaryPreference
    activity_level: ActivityLevel = ActivityLevel.moderate


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=10, le=100)
    height: Optional[float] = Field(None, gt=50, le=300)
    weight: Optional[float] = Field(None, gt=20, le=500)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    fitness_goal: Optional[FitnessGoal] = None
    dietary_preference: Optional[DietaryPreference] = None
    activity_level: Optional[ActivityLevel] = None


# --- Response Models ---

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    gender: str
    age: int
    height: float
    weight: float
    phone: str
    fitness_goal: str
    dietary_preference: str
    activity_level: str
    role: str
    membership_type: str
    is_active: bool
    premium_activated_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
