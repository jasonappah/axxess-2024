from datetime import timedelta
import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = f"Gia API - {os.getenv('ENV', 'development').capitalize()}"
    DESCRIPTION: str = "API for Gia, the prescription management system."
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = "sqlite:///data/database.db"
    API_USERNAME: str = "svc_test"
    API_PASSWORD: str = "superstrongpassword"

    CREATE_NEW_CHAT_SESSION_IF_LAST_MSG_OLDER_THAN: timedelta = timedelta(minutes=5)

    class Config:
        case_sensitive = True


settings = Settings()


class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()