from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    # DATABASE_URL = "sqlite:///./app.db"
    JWT_SECRET_KEY: str = "change-me-super-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 2 * 1024 * 1024
    ALLOWED_UPLOAD_TYPES: str = "image/png,image/jpeg,application/pdf"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
