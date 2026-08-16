from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class FoodCategory(str, Enum):
    protein = "protein"
    carbohydrate = "carbohydrate"
    fiber = "fiber"
    fat = "fat"
    vegetable = "vegetable"
    fruit = "fruit"
    dairy = "dairy"


class Food(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    calories_per_100g: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    dietary_tags: List[str] = []
    description: str
    serving_suggestion: Optional[str] = None


class FoodCreate(BaseModel):
    name: str = Field(..., min_length=2)
    category: FoodCategory
    calories_per_100g: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    fat_g: float = Field(..., ge=0)
    fiber_g: float = Field(..., ge=0)
    dietary_tags: List[str] = []
    description: str = Field(..., min_length=5)
    serving_suggestion: Optional[str] = None


class FoodUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[FoodCategory] = None
    calories_per_100g: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    fiber_g: Optional[float] = Field(None, ge=0)
    dietary_tags: Optional[List[str]] = None
    description: Optional[str] = None
    serving_suggestion: Optional[str] = None
