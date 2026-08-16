from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from app.models.workout import WorkoutPlan, WorkoutPlanCreate, WorkoutPlanUpdate
from app.services.auth_service import get_current_user
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/workouts", tags=["Workouts"])

DAYS_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def serialize_workout(w: dict) -> dict:
    return {
        "id": str(w["_id"]),
        "day": w["day"],
        "gender": w["gender"],
        "focus": w.get("focus", ""),
        "description": w.get("description", ""),
        "exercises": w.get("exercises", []),
    }


def get_current_day() -> str:
    day_num = datetime.now().weekday()  # 0=Monday, 6=Sunday
    return DAYS_ORDER[day_num]


@router.get("/today")
async def get_today_workout(current_user=Depends(get_current_user), db=Depends(get_db)):
    day = get_current_day()
    if day == "sunday":
        return {"day": "sunday", "is_rest_day": True, "message": "Today is your Rest Day! Recovery is just as important as training. 💪"}

    gender = current_user.get("gender", "male").lower()
    workout = await db.workouts.find_one({"day": day, "gender": gender})
    if not workout:
        # Fallback: try the other gender's plan
        workout = await db.workouts.find_one({"day": day})

    if not workout:
        raise HTTPException(status_code=404, detail=f"No workout plan found for {day}")

    return {"day": day, "is_rest_day": False, **serialize_workout(workout)}


@router.get("/week")
async def get_week_workout(current_user=Depends(get_current_user), db=Depends(get_db)):
    gender = current_user.get("gender", "male").lower()
    cursor = db.workouts.find({"gender": gender})
    workouts = await cursor.to_list(length=100)

    result = {}
    for w in workouts:
        result[w["day"]] = serialize_workout(w)

    # Add Sunday rest day
    result["sunday"] = {"day": "sunday", "is_rest_day": True, "message": "Rest Day — Recover and recharge!"}

    current_day = get_current_day()
    return {"workouts": result, "current_day": current_day, "gender": gender}


@router.get("/{day}")
async def get_day_workout(day: str, current_user=Depends(get_current_user), db=Depends(get_db)):
    day = day.lower()
    if day == "sunday":
        return {"day": "sunday", "is_rest_day": True, "message": "Sunday is your Rest Day! Take it easy."}

    gender = current_user.get("gender", "male").lower()
    workout = await db.workouts.find_one({"day": day, "gender": gender})
    if not workout:
        raise HTTPException(status_code=404, detail=f"No workout found for {day}")

    return {"is_rest_day": False, **serialize_workout(workout)}
