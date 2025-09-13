"""
Application settings and environment configuration.
"""
import os
from typing import Optional

class Settings:
    """Application settings class."""
    
    def __init__(self):
        self.huggingface_token: Optional[str] = os.getenv("HUGGINGFACE_HUB_TOKEN")
        self.cuda_available: bool = self._check_cuda()
        self.device: str = "cuda" if self.cuda_available else "cpu"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
    def _check_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.huggingface_token:
            raise RuntimeError("HUGGINGFACE_HUB_TOKEN is not set in the environment")

# Global settings instance
settings = Settings()
