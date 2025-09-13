"""
Application settings and environment configuration.
"""

import os
import torch
from typing import Optional
from config.constants import (
    MODEL_ID, DEFAULT_HOST, DEFAULT_PORT, 
    DEFAULT_MAX_CONCURRENT_GENERATIONS, DEFAULT_GENERATION_TIMEOUT
)

class Settings:
    """Application settings class."""

    def __init__(self):
        self.huggingface_hub_token: Optional[str] = os.getenv("HUGGINGFACE_HUB_TOKEN")
        self.cuda_available: bool = self._check_cuda()
        self.device: str = "cuda" if self.cuda_available else "cpu"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Server configuration - use constants for defaults
        self.host: str = os.getenv("HOST", DEFAULT_HOST)
        self.port: int = int(os.getenv("PORT", str(DEFAULT_PORT)))
        
        # Model configuration - use constant for default
        self.model_id: str = os.getenv("MODEL_ID", MODEL_ID)
        
        # Video generation settings - use constants for defaults
        self.max_concurrent_generations: int = int(os.getenv("MAX_CONCURRENT_GENERATIONS", str(DEFAULT_MAX_CONCURRENT_GENERATIONS)))
        self.generation_timeout: int = int(os.getenv("GENERATION_TIMEOUT", str(DEFAULT_GENERATION_TIMEOUT)))

    def _check_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            return torch.cuda.is_available()
        except ImportError:
            return False

    def validate(self) -> None:
        """Validate required settings."""
        if not self.huggingface_hub_token:
            raise RuntimeError("HUGGINGFACE_HUB_TOKEN is not set in the environment")

# Global settings instance
settings = Settings()
