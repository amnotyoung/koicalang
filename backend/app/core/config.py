"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Koica Lang"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"

    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    GOOGLE_CLOUD_PROJECT_ID: str = ""
    GEMINI_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "sqlite:///./koicalang.db"

    # Audio Settings
    MAX_AUDIO_DURATION_SECONDS: int = 30
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_ENCODING: str = "LINEAR16"

    # Language Settings
    DEFAULT_TARGET_LANGUAGE: str = "km"  # Khmer
    SUPPORTED_LANGUAGES: List[str] = ["km", "lo", "vi"]

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
