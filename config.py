"""Application configuration management."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS Settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Database Settings (if needed for future expansion)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # API Settings
    API_TITLE: str = "Notes API"
    API_DESCRIPTION: str = "A simple FastAPI application for managing notes."
    API_VERSION: str = "1.0.0"
    
    def validate_required_settings(self) -> None:
        """Validate that all required settings are present."""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required")


# Global settings instance
settings = Settings()

# Validate settings on import
settings.validate_required_settings()