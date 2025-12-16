from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import notes_router

def create_app() -> FastAPI:
    """Factory pour créer l'application FastAPI"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description="API REST pour la gestion de notes avec architecture clean"
    )

    # Configuration CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Enregistrement des routes
    app.include_router(notes_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {
            "message": f"Bienvenue sur {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs"
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )