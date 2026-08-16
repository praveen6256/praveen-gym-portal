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
    created_at_val = user.get("created_at")
    if isinstance(created_at_val, datetime):
        created_at_str = created_at_val.isoformat()
    elif isinstance(created_at_val, str):
        created_at_str = created_at_val
    else:
        created_at_str = datetime.now(timezone.utc).isoformat()

    prem_val = user.get("premium_activated_at")
    if isinstance(prem_val, datetime):
        prem_str = prem_val.isoformat()
    elif isinstance(prem_val, str):
        prem_str = prem_val
    else:
        prem_str = None

    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "gender": user.get("gender", "male"),
        "age": user.get("age", 20),
        "height": user.get("height", 170.0),
        "weight": user.get("weight", 70.0),
        "phone": user.get("phone", ""),
        "fitness_goal": user.get("fitness_goal", "maintain"),
        "dietary_preference": user.get("dietary_preference", "vegetarian"),
        "activity_level": user.get("activity_level", "moderate"),
        "role": user.get("role", "member"),
        "membership_type": user.get("membership_type", "standard"),
        "is_active": user.get("is_active", True),
        "premium_activated_at": prem_str,
        "created_at": created_at_str,
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


@router.post("/login")
async def login(credentials: UserLogin, db=Depends(get_db)):
    from fastapi.responses import JSONResponse
    import traceback
    try:
        if db is None:
            return JSONResponse(status_code=500, content={"detail": "Database connection is None"})
            
        email = credentials.email.lower().strip()
        try:
            user = await db.users.find_one({"email": email})
        except Exception as dbe:
            return JSONResponse(status_code=500, content={"error": f"DB Find Error: {str(dbe)}", "traceback": traceback.format_exc().splitlines()})
            
        if not user:
            return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})
            
        try:
            import bcrypt as _b
            hp = user.get("hashed_password", "")
            if not hp or not _b.checkpw(credentials.password.encode('utf-8'), hp.encode('utf-8')):
                return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})
        except Exception as bce:
            return JSONResponse(status_code=500, content={"error": f"Bcrypt Check Error: {str(bce)}", "traceback": traceback.format_exc().splitlines()})

        try:
            token = create_access_token({"sub": str(user["_id"]), "role": user.get("role", "member")})
            ser_user = serialize_user(user)
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": ser_user
            }
        except Exception as te:
            return JSONResponse(status_code=500, content={"error": f"Token/Serialize Error: {str(te)}", "traceback": traceback.format_exc().splitlines()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc().splitlines()})


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return UserResponse(**serialize_user(current_user))
