import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API configuration
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/app_db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "insecure_key_for_dev_only")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "insecure_jwt_key_for_dev_only")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRES_MINUTES", "1440"))  # 24 hours
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()