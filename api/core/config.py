"""
Application configuration
Loads environment variables and provides config settings
"""

import os
from typing import List


class Settings:
    """Application settings loaded from environment variables"""

    # Environment
    ENV: str = os.getenv("ENV", "development")

    # API Security
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "")

    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")

    # Server
    PORT: int = int(os.getenv("PORT", "8080"))

    # Production detection (Vercel)
    IS_PRODUCTION: bool = os.getenv("VERCEL_ENV") == "production"

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENV == "development"


# Global settings instance
settings = Settings()
