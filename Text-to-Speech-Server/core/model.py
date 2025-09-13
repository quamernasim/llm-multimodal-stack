"""
Model initialization and management for Orpheus TTS.
"""
import logging
from typing import Optional
from orpheus_tts import OrpheusModel
from huggingface_hub import login

from config.constants import (
    MODEL_NAME, MAX_MODEL_LENGTH, GPU_MEMORY_UTILIZATION, MAX_NUM_SEQUENCES
)
from config.settings import settings

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the Orpheus TTS model lifecycle."""
    
    def __init__(self):
        self.model: Optional[OrpheusModel] = None
        self._is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the TTS model and authenticate with Hugging Face."""
        if self._is_initialized:
            return
        
        logger.info("Starting model initialization...")
        
        # Validate settings
        settings.validate()
        
        # Authenticate with Hugging Face
        await self._authenticate_huggingface()
        
        # Initialize model
        await self._initialize_model()
        
        self._is_initialized = True
        logger.info("Model initialization completed successfully")
    
    async def _authenticate_huggingface(self) -> None:
        """Authenticate with Hugging Face Hub."""
        try:
            login(token=settings.huggingface_token)
            logger.info("Successfully authenticated with Hugging Face")
        except Exception as e:
            logger.error(f"Failed to authenticate with Hugging Face: {e}")
            raise
    
    async def _initialize_model(self) -> None:
        """Initialize the Orpheus TTS model."""
        try:
            logger.info(f"Initializing Orpheus TTS model on device: {settings.device}")
            self.model = OrpheusModel(
                model_name=MODEL_NAME,
                device=settings.device,
                max_model_len=MAX_MODEL_LENGTH,
                dtype="bfloat16",
                gpu_memory_utilization=GPU_MEMORY_UTILIZATION,
                max_num_seqs=MAX_NUM_SEQUENCES,
            )
            logger.info("Orpheus TTS model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise
    
    def get_model(self) -> OrpheusModel:
        """Get the initialized model instance."""
        if not self._is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        return self.model
    
    async def cleanup(self) -> None:
        """Cleanup model resources."""
        if self.model:
            # Add any cleanup logic here if needed
            pass
        logger.info("Model cleanup completed")

# Global model manager instance
model_manager = ModelManager()
