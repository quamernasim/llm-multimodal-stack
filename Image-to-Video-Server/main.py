"""
Main FastAPI application for Wan Image-to-Video service.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from utils.logging import setup_logging
from core.model import ModelManager, set_model_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    logger.info("Starting Wan Image-to-Video service")
    setup_logging()
    
    # Initialize model manager
    model_manager = ModelManager()
    await model_manager.initialize()
    set_model_manager(model_manager)
    
    logger.info("Service initialization completed")
    yield
    
    logger.info("Shutting down service")
    await model_manager.cleanup()

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Wan Image-to-Video Service",
        description="Generate videos from images using Wan 2.1 I2V model",
        version="1.0.0",
        lifespan=lifespan,
        root_path="/generate"
    )
    
    # Include API routes
    from api.endpoints import video, health
    app.include_router(video.router)
    app.include_router(health.router)
    
    logger.info("FastAPI application created successfully")
    return app

app = create_app()
