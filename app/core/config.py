from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings(BaseSettings):
    # Application
    app_name: str = Field(default="Notes API", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    data_file_path: str = Field(default="data/notes.json", alias="DATA_FILE_PATH")
    
    # Messages API
    api_welcome_message: str = Field(default="Bienvenue sur {app_name}", alias="API_WELCOME_MESSAGE")
    api_health_status: str = Field(default="healthy", alias="API_HEALTH_STATUS")
    api_docs_path: str = Field(default="/docs", alias="API_DOCS_PATH")
    
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def allowed_origins(self) -> List[str]:
        """Parse CORS origins from environment variable or use defaults"""
        origins_env = os.getenv("CORS_ORIGINS", "")
        if origins_env:
            return [origin.strip() for origin in origins_env.split(",")]
        
        # Utiliser les valeurs par défaut depuis les variables d'environnement
        default_origins = os.getenv("DEFAULT_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        return [origin.strip() for origin in default_origins.split(",")]

settings = Settings()