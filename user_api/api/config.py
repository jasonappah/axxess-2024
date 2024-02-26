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
    DATABASE_URI: str = "postgresql+psycopg2://dev_api_admin:dev_api_admin@postgres:5432/gia_dev"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    API_USERNAME: str = "svc_test"
    API_PASSWORD: str = "superstrongpassword"

    CREATE_NEW_CHAT_SESSION_IF_LAST_MSG_OLDER_THAN: timedelta = timedelta(minutes=5)

    # set base url to none to use the default openai api url, or set it to a custom url in .env file to use Ollama or other OpenAI-compatible API
    OPENAI_API_KEY: str = "__OLLAMA__"
    OPENAI_BASE_URL: str | None = None
    # OPENAI_BASE_URL: str | None = "http://localhost:11434/v1"
    OPENAI_MODEL_ID: str = "mistral"

    class Config:
        case_sensitive = True


settings = Settings()


class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
