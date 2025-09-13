"""
Main FastAPI application with lifespan management.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.model import model_manager
from api.endpoints import synthesis, voices, health
from utils.logging import setup_logging

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
        title="Orpheus TTS Service",
        description="Text-to-Speech service using Orpheus TTS model",
        version="1.0.0",
        lifespan=lifespan,
        root_path="/synthesize"
    )
    
    # Include routers
    app.include_router(synthesis.router)
    app.include_router(voices.router)
    app.include_router(health.router)
    
    return app

app = create_app()
