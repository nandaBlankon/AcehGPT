from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aceh GPT Backend"
    API_V1_STR: str = "/api/v1"
    
    # Security / CORS settings
    # Conforming to secure coding guidelines: No wildcard '*' in CORS.
    # Commas-separated list of origins will be automatically parsed to a list.
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ],
        description="List of allowed CORS origins"
    )
    
    # Vector DB / Turbovec Settings
    TURBOVEC_API_KEY: str = Field(default="", description="API Key for Turbovec vector database")
    TURBOVEC_HOST: str = Field(default="http://localhost:8080", description="Turbovec host URL")
    
    # Model Settings
    MODEL_NAME: str = Field(default="indobenchmark/indogpt", description="LLM model name or path")
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding model name or path")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
