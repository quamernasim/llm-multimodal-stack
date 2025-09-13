"""
Model initialization and management for BLIP-2.
"""

import logging
import torch
from typing import Optional
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from huggingface_hub import login

from config.constants import MODEL_NAME, MODEL_PRECISION
from config.settings import settings

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the BLIP-2 model lifecycle."""

    def __init__(self):
        self.model: Optional[Blip2ForConditionalGeneration] = None
        self.processor: Optional[Blip2Processor] = None
        self._is_initialized = False

    async def initialize(self) -> None:
        """Initialize the BLIP-2 model and authenticate with Hugging Face."""
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
        """Initialize the BLIP-2 model."""
        try:
            logger.info(f"Initializing BLIP-2 model: {MODEL_NAME} on device: {settings.device}")

            # Load processor
            self.processor = Blip2Processor.from_pretrained(MODEL_NAME)

            # Load model with float16 precision
            self.model = Blip2ForConditionalGeneration.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto"
            )

            logger.info("BLIP-2 model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise

    def get_model(self) -> Blip2ForConditionalGeneration:
        """Get the initialized model instance."""
        if not self._is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        return self.model

    def get_processor(self) -> Blip2Processor:
        """Get the initialized processor instance."""
        if not self._is_initialized or self.processor is None:
            raise RuntimeError("Processor not initialized. Call initialize() first.")
        return self.processor

    async def cleanup(self) -> None:
        """Cleanup model resources."""
        if self.model:
            # Clear CUDA cache if using GPU
            if settings.cuda_available:
                torch.cuda.empty_cache()
        logger.info("Model cleanup completed")

# Global model manager instance
model_manager = ModelManager()