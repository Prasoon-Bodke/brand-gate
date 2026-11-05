from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Brand Gate"
    API_V1_STR: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/brand_gate"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_ANON_KEY: str = ""

    # AI Pipeline
    JEV_MODEL_ENDPOINT: str = "http://localhost:8001/jev"
    LITELLM_MASTER_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    QWEN_LLM_MODEL: str = "qwen2.5:7b"
    LLAMA_LLM_MODEL: str = "llama3.2:3b"

    # Vision & OCR
    PADDLEOCR_ENABLED: bool = True
    DOCLING_ENABLED: bool = True
    SIGLIP_MODEL_PATH: str = "google/siglip-base-patch16-224"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()