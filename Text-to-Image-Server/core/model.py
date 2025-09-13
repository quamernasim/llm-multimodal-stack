"""
Model initialization and management for FLUX Text-to-Image.
"""
import logging
import torch
from typing import Optional
from diffusers import FluxPipeline
from huggingface_hub import login

from config.constants import MODEL_NAME
from config.settings import settings

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the FLUX model lifecycle."""
    
    def __init__(self):
        self.pipeline: Optional[FluxPipeline] = None
        self._is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the FLUX pipeline and authenticate with Hugging Face."""
        if self._is_initialized:
            return
        
        logger.info("Starting model initialization...")
        
        # Validate settings
        settings.validate()
        
        # Authenticate with Hugging Face
        await self._authenticate_huggingface()
        
        # Initialize pipeline
        await self._initialize_pipeline()
        
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
    
    async def _initialize_pipeline(self) -> None:
        """Initialize the FLUX pipeline."""
        try:
            logger.info(f"Loading FLUX model: {MODEL_NAME}")
            logger.info(f"Using device: {settings.device}")
            logger.info(f"VRAM available: {settings.vram_gb:.2f} GB")
            
            # Load pipeline
            self.pipeline = FluxPipeline.from_pretrained(
                MODEL_NAME, 
                torch_dtype=settings.torch_dtype
            )
            
            # Configure pipeline based on available memory
            if settings.enable_cpu_offload:
                self.pipeline.enable_model_cpu_offload()
                logger.info("Using CPU offloading for memory optimization")
            else:
                self.pipeline = self.pipeline.to(settings.device)
                logger.info("Using full GPU acceleration")
            
            logger.info("FLUX pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            raise
    
    def get_pipeline(self) -> FluxPipeline:
        """Get the initialized pipeline instance."""
        if not self._is_initialized or self.pipeline is None:
            raise RuntimeError("Pipeline not initialized. Call initialize() first.")
        return self.pipeline
    
    def get_device(self) -> str:
        """Get the device being used."""
        return settings.device
    
    async def cleanup(self) -> None:
        """Cleanup pipeline resources."""
        if self.pipeline:
            # Move pipeline to CPU to free GPU memory
            try:
                if hasattr(self.pipeline, 'to'):
                    self.pipeline.to('cpu')
                del self.pipeline
                self.pipeline = None
                
                # Clear CUDA cache if using GPU
                if settings.cuda_available:
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
                    
            except Exception as e:
                logger.warning(f"Error during pipeline cleanup: {e}")
        
        logger.info("Model cleanup completed")

# Global model manager instance
model_manager = ModelManager()
