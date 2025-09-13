"""
Main FastAPI application with lifespan management.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.model import model_manager
from api.endpoints import caption, health
from utils.logging import setup_logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting BLIP-2 Image-to-Text Service...")
    setup_logging()
    await model_manager.initialize()
    yield
    # Shutdown
    logger.info("Shutting down BLIP-2 Image-to-Text Service...")
    await model_manager.cleanup()

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="BLIP-2 Image-to-Text Service",
        description="Image captioning service using BLIP-2 model",
        version="1.0.0",
        lifespan=lifespan,
        root_path="/caption"
    )

    # Include routers
    app.include_router(caption.router)
    app.include_router(health.router)

    return app

app = create_app()