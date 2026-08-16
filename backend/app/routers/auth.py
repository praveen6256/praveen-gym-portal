from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from datetime import datetime, timezone
from app.config import get_settings
from app.models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import (
    hash_password, verify_password, create_access_token, get_current_user
)
from app.services.email_service import send_registration_email
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
        "premium_activated_at": user.get("premium_activated_at").isoformat() if user.get("premium_activated_at") else None,
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else datetime.now(timezone.utc).isoformat(),
    }


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, background_tasks: BackgroundTasks, db=Depends(get_db)):
    # Check existing email
    existing = await db.users.find_one({"email": user_data.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    now = datetime.now(timezone.utc)
    user_doc = {
        "name": user_data.name.strip(),
        "email": user_data.email.lower(),
        "hashed_password": hash_password(user_data.password),
        "gender": user_data.gender.value,
        "age": user_data.age,
        "height": user_data.height,
        "weight": user_data.weight,
        "phone": user_data.phone,
        "fitness_goal": user_data.fitness_goal.value,
        "dietary_preference": user_data.dietary_preference.value,
        "activity_level": user_data.activity_level.value,
        "role": "member",
        "membership_type": "standard",
        "is_active": True,
        "premium_activated_at": None,
        "premium_activated_by": None,
        "created_at": now,
        "updated_at": now,
    }

    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token({"sub": str(result.inserted_id), "role": "member"})

    if get_settings().RESEND_API_KEY:
        background_tasks.add_task(
            send_registration_email,
            name=user_data.name,
            email=user_data.email,
            membership_type="standard",
        )

    return TokenResponse(
        access_token=token,
        user=UserResponse(**serialize_user(user_doc)),
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db=Depends(get_db)):
    try:
        user = await db.users.find_one({"email": credentials.email.lower()})
        if not user or not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not user.get("is_active", True):
            raise HTTPException(status_code=403, detail="Account has been disabled. Please contact the gym.")

        token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})

        return TokenResponse(
            access_token=token,
            user=UserResponse(**serialize_user(user)),
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"Login error: {tb}")
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)} | TB: {tb}")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return UserResponse(**serialize_user(current_user))
