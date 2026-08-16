"""
Create the first Admin account.
Run once locally against your MongoDB Atlas database.

Usage:
  cd backend
  python scripts/create_admin.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin():
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "praveen_gym")

    if not mongo_url:
        print("❌ MONGODB_URL not set in .env file")
        return

    print("Praveen Gym Portal — Admin Account Creator")
    print("=" * 45)
    name = input("Admin Name: ").strip()
    email = input("Admin Email: ").strip().lower()
    password = input("Admin Password (min 8 chars): ").strip()

    if len(password) < 8:
        print("❌ Password must be at least 8 characters")
        return

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    existing = await db.users.find_one({"email": email})
    if existing:
        print(f"❌ An account with email '{email}' already exists.")
        client.close()
        return

    admin_doc = {
        "name": name,
        "email": email,
        "hashed_password": pwd_context.hash(password),
        "gender": "male",
        "age": 30,
        "height": 170,
        "weight": 70,
        "phone": "0000000000",
        "fitness_goal": "maintain",
        "dietary_preference": "non_vegetarian",
        "activity_level": "moderate",
        "role": "admin",
        "membership_type": "premium",
        "is_active": True,
        "premium_activated_at": None,
        "premium_activated_by": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = await db.users.insert_one(admin_doc)
    print(f"\n✅ Admin account created!")
    print(f"   Name  : {name}")
    print(f"   Email : {email}")
    print(f"   ID    : {result.inserted_id}")
    print(f"\nYou can now login at the Admin login page.")

    client.close()


if __name__ == "__main__":
    asyncio.run(create_admin())
