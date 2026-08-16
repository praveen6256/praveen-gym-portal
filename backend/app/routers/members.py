from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from app.models.user import UserUpdate, UserResponse
from app.services.auth_service import get_current_user
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/members", tags=["Members"])


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
        "created_at": user["created_at"],
    }


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user=Depends(get_current_user), db=Depends(get_db)):
    return UserResponse(**serialize_user(current_user))


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Convert enum values to strings
    for k, v in update_fields.items():
        if hasattr(v, "value"):
            update_fields[k] = v.value

    update_fields["updated_at"] = datetime.now(timezone.utc)

    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_fields},
    )

    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    return UserResponse(**serialize_user(updated_user))
