from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application
    app_name: str = "Notes API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Database
    data_file_path: str = "data/notes.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()