"""
Model initialization and management for Whisper Speech-to-Text.
"""
import logging
import torch
from typing import Optional, Tuple
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from config.constants import MODEL_NAME
from config.settings import settings

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the Whisper model lifecycle."""
    
    def __init__(self):
        self.model: Optional[WhisperForConditionalGeneration] = None
        self.processor: Optional[WhisperProcessor] = None
        self._is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the Whisper model and processor."""
        if self._is_initialized:
            return
        
        logger.info("Starting model initialization...")
        
        # Validate settings
        settings.validate()
        
        # Configure torch settings
        if settings.disable_gradients:
            torch.set_grad_enabled(False)
            logger.info("Gradients disabled for inference")
        
        logger.info(f"Using device: {settings.device}")
        
        # Initialize model and processor
        await self._initialize_model()
        
        self._is_initialized = True
        logger.info("Model initialization completed successfully")
    
    async def _initialize_model(self) -> None:
        """Initialize the Whisper model and processor."""
        try:
            logger.info(f"Loading Whisper model: {MODEL_NAME}")
            
            # Load processor
            self.processor = WhisperProcessor.from_pretrained(MODEL_NAME)
            logger.info("Whisper processor loaded successfully")
            
            # Load model
            self.model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME).to(settings.device)
            logger.info("Whisper model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise
    
    def get_model_and_processor(self) -> Tuple[WhisperForConditionalGeneration, WhisperProcessor]:
        """Get the initialized model and processor instances."""
        if not self._is_initialized or self.model is None or self.processor is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        return self.model, self.processor
    
    def get_device(self) -> str:
        """Get the device being used."""
        return settings.device
    
    async def cleanup(self) -> None:
        """Cleanup model resources."""
        if self.model:
            # Move model to CPU to free GPU memory
            self.model.cpu()
            del self.model
            self.model = None
        if self.processor:
            del self.processor
            self.processor = None
        
        # Clear CUDA cache if using GPU
        if settings.cuda_available:
            torch.cuda.empty_cache()
        
        logger.info("Model cleanup completed")

# Global model manager instance
model_manager = ModelManager()
