from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class Exercise(BaseModel):
    name: str
    description: str
    image_url: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_minutes: Optional[int] = None
    rest_seconds: int = 60
    muscle_group: Optional[str] = None


class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=2)
    description: str = Field(..., min_length=10)
    image_url: str
    sets: Optional[int] = Field(None, ge=1, le=20)
    reps: Optional[int] = Field(None, ge=1, le=200)
    duration_minutes: Optional[int] = Field(None, ge=1, le=120)
    rest_seconds: int = Field(60, ge=0, le=600)
    muscle_group: Optional[str] = None


class WorkoutPlan(BaseModel):
    id: Optional[str] = None
    day: str
    gender: str
    focus: str
    description: str
    exercises: List[Exercise] = []


class WorkoutPlanCreate(BaseModel):
    day: DayOfWeek
    gender: str = Field(..., pattern="^(male|female)$")
    focus: str = Field(..., min_length=2)
    description: str = Field(..., min_length=10)
    exercises: List[ExerciseCreate] = []


class WorkoutPlanUpdate(BaseModel):
    focus: Optional[str] = None
    description: Optional[str] = None
    exercises: Optional[List[ExerciseCreate]] = None
