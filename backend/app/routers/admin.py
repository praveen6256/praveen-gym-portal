from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId
from app.services.auth_service import get_current_admin
from app.services.email_service import send_premium_activation_email
from app.models.workout import WorkoutPlanCreate, WorkoutPlanUpdate
from app.models.food import FoodCreate, FoodUpdate
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "gender": user["gender"],
        "age": user["age"],
        "height": user["height"],
        "weight": user["weight"],
        "phone": user["phone"],
        "fitness_goal": user["fitness_goal"],
        "dietary_preference": user["dietary_preference"],
        "activity_level": user.get("activity_level", "moderate"),
        "role": user["role"],
        "membership_type": user["membership_type"],
        "is_active": user.get("is_active", True),
        "premium_activated_at": user.get("premium_activated_at"),
        "premium_activated_by": user.get("premium_activated_by"),
        "created_at": user["created_at"],
    }


def serialize_workout(w: dict) -> dict:
    return {
        "id": str(w["_id"]),
        "day": w["day"],
        "gender": w["gender"],
        "focus": w.get("focus", ""),
        "description": w.get("description", ""),
        "exercises": w.get("exercises", []),
    }


def serialize_food(f: dict) -> dict:
    return {
        "id": str(f["_id"]),
        "name": f["name"],
        "category": f["category"],
        "calories_per_100g": f["calories_per_100g"],
        "protein_g": f["protein_g"],
        "carbs_g": f["carbs_g"],
        "fat_g": f["fat_g"],
        "fiber_g": f["fiber_g"],
        "dietary_tags": f.get("dietary_tags", []),
        "description": f["description"],
        "serving_suggestion": f.get("serving_suggestion"),
    }


# ─── Dashboard Stats ────────────────────────────────────────────────────────

@router.get("/dashboard/stats")
async def get_dashboard_stats(admin=Depends(get_current_admin), db=Depends(get_db)):
    total = await db.users.count_documents({"role": "member"})
    standard = await db.users.count_documents({"role": "member", "membership_type": "standard"})
    premium = await db.users.count_documents({"role": "member", "membership_type": "premium"})
    active = await db.users.count_documents({"role": "member", "is_active": True})
    inactive = await db.users.count_documents({"role": "member", "is_active": False})
    male = await db.users.count_documents({"role": "member", "gender": "male"})
    female = await db.users.count_documents({"role": "member", "gender": "female"})

    # Recent 5 members
    cursor = db.users.find({"role": "member"}).sort("created_at", -1).limit(5)
    recent = await cursor.to_list(length=5)

    return {
        "total_members": total,
        "standard_members": standard,
        "premium_members": premium,
        "active_members": active,
        "inactive_members": inactive,
        "male_members": male,
        "female_members": female,
        "recent_registrations": [serialize_user(u) for u in recent],
    }


# ─── Members Management ───────────────────────────────────────────────────

@router.get("/members")
async def list_members(
    search: Optional[str] = Query(None),
    membership_type: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    query = {"role": "member"}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
        ]
    if membership_type:
        query["membership_type"] = membership_type
    if gender:
        query["gender"] = gender.lower()
    if is_active is not None:
        query["is_active"] = is_active

    total = await db.users.count_documents(query)
    cursor = db.users.find(query).sort("created_at", -1).skip(skip).limit(limit)
    members = await cursor.to_list(length=limit)

    return {"total": total, "members": [serialize_user(m) for m in members]}


@router.get("/members/{member_id}")
async def get_member(member_id: str, admin=Depends(get_current_admin), db=Depends(get_db)):
    try:
        user = await db.users.find_one({"_id": ObjectId(member_id), "role": "member"})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid member ID")
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    return serialize_user(user)


@router.post("/members/{member_id}/activate-premium")
async def activate_premium(
    member_id: str,
    background_tasks: BackgroundTasks,
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    try:
        obj_id = ObjectId(member_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid member ID")

    user = await db.users.find_one({"_id": obj_id, "role": "member"})
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    if user.get("membership_type") == "premium":
        raise HTTPException(status_code=400, detail="Member already has Premium membership")

    now = datetime.now(timezone.utc)
    await db.users.update_one(
        {"_id": obj_id},
        {
            "$set": {
                "membership_type": "premium",
                "premium_activated_at": now,
                "premium_activated_by": str(admin["_id"]),
                "updated_at": now,
            }
        },
    )

    # Log to membership history
    await db.membership_history.insert_one({
        "user_id": member_id,
        "user_name": user["name"],
        "user_email": user["email"],
        "action": "activated",
        "performed_by": str(admin["_id"]),
        "performed_by_name": admin["name"],
        "performed_at": now,
        "notes": "Premium activated after cash payment at gym counter",
    })

    background_tasks.add_task(
        send_premium_activation_email,
        name=user["name"],
        email=user["email"],
        activated_by=admin["name"],
    )

    return {"message": f"Premium activated for {user['name']}", "activated_at": now}


@router.post("/members/{member_id}/remove-premium")
async def remove_premium(
    member_id: str,
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    try:
        obj_id = ObjectId(member_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid member ID")

    user = await db.users.find_one({"_id": obj_id, "role": "member"})
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")

    now = datetime.now(timezone.utc)
    await db.users.update_one(
        {"_id": obj_id},
        {
            "$set": {
                "membership_type": "standard",
                "premium_activated_at": None,
                "premium_activated_by": None,
                "updated_at": now,
            }
        },
    )

    await db.membership_history.insert_one({
        "user_id": member_id,
        "user_name": user["name"],
        "user_email": user["email"],
        "action": "removed",
        "performed_by": str(admin["_id"]),
        "performed_by_name": admin["name"],
        "performed_at": now,
        "notes": "Premium removed by admin",
    })

    return {"message": f"Premium removed for {user['name']}"}


@router.post("/members/{member_id}/toggle-active")
async def toggle_member_active(
    member_id: str,
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    try:
        obj_id = ObjectId(member_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid member ID")

    user = await db.users.find_one({"_id": obj_id, "role": "member"})
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")

    new_status = not user.get("is_active", True)
    await db.users.update_one(
        {"_id": obj_id},
        {"$set": {"is_active": new_status, "updated_at": datetime.now(timezone.utc)}},
    )

    action = "enabled" if new_status else "disabled"
    return {"message": f"Account {action} for {user['name']}", "is_active": new_status}


# ─── Membership History ───────────────────────────────────────────────────

@router.get("/membership-history")
async def get_membership_history(
    skip: int = 0, limit: int = 50, admin=Depends(get_current_admin), db=Depends(get_db)
):
    cursor = db.membership_history.find().sort("performed_at", -1).skip(skip).limit(limit)
    history = await cursor.to_list(length=limit)
    total = await db.membership_history.count_documents({})
    for h in history:
        h["id"] = str(h.pop("_id"))
    return {"total": total, "history": history}


# ─── Workout Management ───────────────────────────────────────────────────

@router.get("/workouts")
async def list_workouts(
    gender: Optional[str] = Query(None),
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    query = {}
    if gender:
        query["gender"] = gender.lower()
    cursor = db.workouts.find(query).sort([("gender", 1), ("day", 1)])
    workouts = await cursor.to_list(length=100)
    return [serialize_workout(w) for w in workouts]


@router.post("/workouts", status_code=201)
async def create_workout(
    plan: WorkoutPlanCreate,
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    existing = await db.workouts.find_one({"day": plan.day.value, "gender": plan.gender})
    if existing:
        raise HTTPException(status_code=400, detail=f"Workout plan for {plan.day}/{plan.gender} already exists. Use PUT to update.")

    doc = plan.model_dump()
    doc["day"] = plan.day.value
    doc["created_at"] = datetime.now(timezone.utc)

    result = await db.workouts.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_workout(doc)


@router.put("/workouts/{workout_id}")
async def update_workout(
    workout_id: str,
    update: WorkoutPlanUpdate,
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    try:
        obj_id = ObjectId(workout_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid workout ID")

    update_fields = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await db.workouts.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Workout not found")
    return serialize_workout(result)


@router.delete("/workouts/{workout_id}", status_code=204)
async def delete_workout(workout_id: str, admin=Depends(get_current_admin), db=Depends(get_db)):
    try:
        result = await db.workouts.delete_one({"_id": ObjectId(workout_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid workout ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")


# ─── Food Management ───────────────────────────────────────────────────────

@router.get("/foods")
async def list_foods(
    category: Optional[str] = Query(None),
    admin=Depends(get_current_admin),
    db=Depends(get_db),
):
    query = {}
    if category:
        query["category"] = category
    cursor = db.foods.find(query).sort("name", 1)
    foods = await cursor.to_list(length=500)
    return [serialize_food(f) for f in foods]


@router.post("/foods", status_code=201)
async def create_food(food: FoodCreate, admin=Depends(get_current_admin), db=Depends(get_db)):
    doc = food.model_dump()
    doc["category"] = food.category.value
    doc["created_at"] = datetime.now(timezone.utc)
    result = await db.foods.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_food(doc)


@router.put("/foods/{food_id}")
async def update_food(
    food_id: str, update: FoodUpdate, admin=Depends(get_current_admin), db=Depends(get_db)
):
    try:
        obj_id = ObjectId(food_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid food ID")

    update_fields = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    if "category" in update_fields and hasattr(update_fields["category"], "value"):
        update_fields["category"] = update_fields["category"].value
    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await db.foods.find_one_and_update(
        {"_id": obj_id}, {"$set": update_fields}, return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Food not found")
    return serialize_food(result)


@router.delete("/foods/{food_id}", status_code=204)
async def delete_food(food_id: str, admin=Depends(get_current_admin), db=Depends(get_db)):
    try:
        result = await db.foods.delete_one({"_id": ObjectId(food_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid food ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Food not found")
