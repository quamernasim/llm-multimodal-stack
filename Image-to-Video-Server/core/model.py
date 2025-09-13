"""
Model management for Wan Image-to-Video pipeline.
"""

import torch
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from transformers import CLIPVisionModel
from config.constants import MODEL_ID, MODEL_PRECISION, VAE_PRECISION, IMAGE_ENCODER_PRECISION
from config.settings import settings
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages Wan Image-to-Video model lifecycle."""
    
    def __init__(self):
        self.pipeline: Optional[WanImageToVideoPipeline] = None
        self.device = None
    
    async def initialize(self):
        """Initialize the Wan Image-to-Video pipeline."""
        try:
            logger.info("Initializing Wan Image-to-Video model")
            
            # Set device
            self.device = settings.device
            logger.info(f"Using device: {self.device}")
            
            # Load image encoder
            image_encoder = CLIPVisionModel.from_pretrained(
                MODEL_ID,
                subfolder="image_encoder",
                torch_dtype=getattr(torch, IMAGE_ENCODER_PRECISION),
                token=settings.huggingface_hub_token
            )
            
            # Load VAE
            vae = AutoencoderKLWan.from_pretrained(
                MODEL_ID,
                subfolder="vae",
                torch_dtype=getattr(torch, VAE_PRECISION),
                token=settings.huggingface_hub_token
            )
            
            # Load pipeline
            self.pipeline = WanImageToVideoPipeline.from_pretrained(
                MODEL_ID,
                vae=vae,
                image_encoder=image_encoder,
                torch_dtype=getattr(torch, MODEL_PRECISION),
                token=settings.huggingface_hub_token,
                use_safetensors=True,
            )
            
            # Move to device
            self.pipeline.to(self.device)
            
            logger.info("Model initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise
    
    async def get_pipeline(self) -> WanImageToVideoPipeline:
        """Get the loaded pipeline."""
        if self.pipeline is None:
            raise RuntimeError("Pipeline not initialized")
        return self.pipeline
    
    async def cleanup(self):
        """Clean up model resources."""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info("Model cleanup completed")

# Global model manager instance
_model_manager: Optional[ModelManager] = None

async def get_model_manager() -> ModelManager:
    """Dependency function to get the model manager."""
    global _model_manager
    if _model_manager is None:
        raise RuntimeError("Model manager not initialized")
    return _model_manager

def set_model_manager(manager: ModelManager):
    """Set the global model manager instance."""
    global _model_manager
    _model_manager = manager
