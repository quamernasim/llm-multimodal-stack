"""
Health check functionality.
"""
import logging
import torch
from typing import Dict, Any
from config.constants import MODEL_NAME, VALID_VOICES
from config.settings import settings

logger = logging.getLogger(__name__)

class HealthChecker:
    """Provides health check functionality."""
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        try:
            health_info = {
                "status": "healthy",
                "service": "Orpheus TTS Service",
                "model_name": MODEL_NAME,
                "device": settings.device,
                "cuda_available": settings.cuda_available,
                "supported_voices": VALID_VOICES
            }
            
            # Add CUDA-specific information if available
            if settings.cuda_available:
                health_info.update(self._get_cuda_info())
            
            logger.info("Health check completed successfully")
            return health_info
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _get_cuda_info(self) -> Dict[str, Any]:
        """Get CUDA-specific information."""
        return {
            "cuda_device_count": torch.cuda.device_count(),
            "cuda_device_name": torch.cuda.get_device_name(),
            "cuda_memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
            "cuda_memory_reserved": f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB"
        }

# Global health checker instance
health_checker = HealthChecker()
