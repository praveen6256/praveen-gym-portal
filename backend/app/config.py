from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://praveenadmin:PraveenGym2026@cluster0.volnmsx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME: str = "praveen_gym"
    JWT_SECRET: str = "praveen_gym_super_secret_jwt_key_2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 30
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@praveengym.com"
    FRONTEND_URL: str = "http://localhost:5173"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
