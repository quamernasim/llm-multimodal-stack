"""
Main FastAPI application with lifespan management.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.model import model_manager
from api.endpoints import transcription, health
from utils.logging import setup_logging
from config.constants import APP_NAME, DESCRIPTION, VERSION

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging()
    await model_manager.initialize()
    yield
    # Shutdown
    await model_manager.cleanup()

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=APP_NAME,
        description=DESCRIPTION,
        version=VERSION,
        lifespan=lifespan,
        root_path="/transcribe"
    )
    
    # Include routers
    app.include_router(transcription.router)
    app.include_router(health.router)
    
    return app

app = create_app()
