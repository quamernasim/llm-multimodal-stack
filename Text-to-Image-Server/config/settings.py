"""
Application settings and environment configuration.
"""
import os
import torch
from typing import Optional

class Settings:
    """Application settings class."""
    
    def __init__(self):
        self.huggingface_token: Optional[str] = os.getenv("HUGGINGFACE_HUB_TOKEN")
        self.cuda_available: bool = self._check_cuda()
        self.device: str = "cuda" if self.cuda_available else "cpu"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.vram_gb: float = self._get_vram_gb()
        self.enable_cpu_offload: bool = self._should_enable_cpu_offload()
        self.torch_dtype = torch.bfloat16
        
    def _check_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            return torch.cuda.is_available()
        except Exception:
            return False
    
    def _get_vram_gb(self) -> float:
        """Get available VRAM in GB."""
        if self.cuda_available:
            try:
                return torch.cuda.get_device_properties(0).total_memory / 1024**3
            except Exception:
                return 0.0
        return 0.0
    
    def _should_enable_cpu_offload(self) -> bool:
        """Determine if CPU offloading should be enabled based on VRAM."""
        from config.constants import HIGH_VRAM_THRESHOLD_GB
        return self.cuda_available and self.vram_gb <= HIGH_VRAM_THRESHOLD_GB
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.huggingface_token:
            raise RuntimeError("HUGGINGFACE_HUB_TOKEN is not set in the environment")

# Global settings instance
settings = Settings()
