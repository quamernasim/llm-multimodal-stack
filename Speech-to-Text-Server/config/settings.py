"""
Application settings and environment configuration.
"""
import os
from typing import Optional

class Settings:
    """Application settings class."""
    
    def __init__(self):
        self.cuda_available: bool = self._check_cuda()
        self.device: str = "cuda" if self.cuda_available else "cpu"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.disable_gradients: bool = os.getenv("DISABLE_GRADIENTS", "true").lower() == "true"
        
    def _check_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def validate(self) -> None:
        """Validate required settings."""
        # Add any validation logic here if needed
        pass

# Global settings instance
settings = Settings()
