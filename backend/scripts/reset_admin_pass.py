import pymongo
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGODB_URL")
client = pymongo.MongoClient(mongo_url)
db = client["praveen_gym"]

new_hash = bcrypt.hashpw(b"Admin12345", bcrypt.gensalt()).decode("utf-8")
db.users.update_one(
    {"email": "admin@praveengym.com"},
    {"$set": {"hashed_password": new_hash}}
)

print("SUCCESS: Admin password reset to Admin12345")
