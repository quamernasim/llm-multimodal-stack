"""
Core image generation functionality.
"""
import io
import time
import logging
import torch
from typing import Tuple, Optional
from PIL import Image

from core.model import model_manager
from config.constants import IMAGE_FORMAT
from config.settings import settings

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Handles image generation operations."""
    
    def generate_image(
        self,
        prompt: str,
        guidance_scale: float,
        num_inference_steps: int,
        max_sequence_length: int,
        seed: Optional[int],
        width: int,
        height: int
    ) -> Tuple[Image.Image, int, float]:
        """
        Generate image from text prompt using the FLUX model.
        
        Args:
            prompt: Text description for image generation
            guidance_scale: How closely to follow the prompt
            num_inference_steps: Number of denoising steps
            max_sequence_length: Maximum sequence length for text encoding
            seed: Random seed for reproducibility
            width: Output image width
            height: Output image height
            
        Returns:
            Tuple of (generated image, seed used, generation time)
            
        Raises:
            Exception: If generation fails
        """
        start_time = time.time()
        logger.info(f"Starting image generation for prompt: '{prompt[:50]}...'")
        
        try:
            pipeline = model_manager.get_pipeline()
            device = model_manager.get_device()
            
            # Set random seed if not provided
            if seed is None:
                seed = torch.randint(0, 2**32 - 1, (1,)).item()
            
            # Create generator with seed
            generator = torch.Generator(device).manual_seed(seed)
            
            # Generate image
            with torch.no_grad():
                result = pipeline(
                    prompt,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    max_sequence_length=max_sequence_length,
                    generator=generator,
                    width=width,
                    height=height
                )
                image = result.images[0]
            
            # Clean up GPU memory
            self._cleanup_gpu_memory()
            
            generation_time = time.time() - start_time
            
            logger.info(
                f"Successfully generated {width}x{height} image in {generation_time:.2f} seconds "
                f"(seed: {seed}, steps: {num_inference_steps})"
            )
            
            return image, seed, generation_time
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            raise
    
    def image_to_bytes(self, image: Image.Image, format: str = IMAGE_FORMAT) -> bytes:
        """
        Convert PIL Image to bytes.
        
        Args:
            image: PIL Image object
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            Image as bytes
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        return buffer.read()
    
    def _cleanup_gpu_memory(self) -> None:
        """Clean up GPU memory after generation."""
        if settings.cuda_available:
            try:
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
            except Exception as e:
                logger.warning(f"GPU memory cleanup warning: {e}")

# Global generator instance
generator = ImageGenerator()
