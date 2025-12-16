from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "Notes API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    data_file_path: str = "data/notes.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
    
    @property
    def allowed_origins(self) -> List[str]:
        """Parse CORS origins from environment variable or use defaults"""
        origins_env = os.getenv("CORS_ORIGINS", "")
        if origins_env:
            return [origin.strip() for origin in origins_env.split(",")]
        return ["http://localhost:5173", "http://127.0.0.1:5173"]

settings = Settings()