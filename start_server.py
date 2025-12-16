#!/usr/bin/env python3
"""
Script de démarrage du serveur FastAPI
"""
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print(f"🚀 Démarrage du serveur {settings.app_name} v{settings.app_version}")
    print(f"📍 URL: http://{settings.host}:{settings.port}")
    print(f"📚 Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"🔧 Mode debug: {settings.debug}")
    print(f"🌐 CORS autorisé pour: {settings.allowed_origins}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )