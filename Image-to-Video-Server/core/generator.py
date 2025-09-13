"""
Core video generation functionality using Wan Image-to-Video pipeline.
"""

import torch
import numpy as np
import tempfile
import uuid
from pathlib import Path
from PIL import Image
from diffusers.utils import export_to_video

from core.model import get_model_manager
from config.constants import (
    MODEL_ID, MAX_AREA_480P, DEFAULT_NUM_FRAMES, 
    DEFAULT_GUIDANCE_SCALE, DEFAULT_FPS, TEMP_VIDEO_DIR, DEFAULT_INFERENCE_STEPS
)
import logging

logger = logging.getLogger(__name__)

class VideoGenerator:
    """Handles video generation using Wan Image-to-Video pipeline."""
    
    def __init__(self):
        # Ensure temp directory exists
        Path(TEMP_VIDEO_DIR).mkdir(exist_ok=True)
    
    async def generate_video_from_image(
        self,
        image: Image.Image,
        prompt: str,
        negative_prompt: str = "",
        num_frames: int = DEFAULT_NUM_FRAMES,
        guidance_scale: float = DEFAULT_GUIDANCE_SCALE,
        fps: int = DEFAULT_FPS,
        num_inference_steps: int = DEFAULT_INFERENCE_STEPS
    ) -> str:
        """Generate video from PIL Image object and return file path."""
        
        try:
            logger.info("Starting video generation")
            
            # Get pipeline
            model_manager = await get_model_manager()
            pipeline = await model_manager.get_pipeline()
            
            # Prepare image dimensions
            image = self._prepare_image_dimensions(image, pipeline)
            
            # Generate video
            with torch.no_grad():
                output = pipeline(
                    image=image,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    height=image.height,
                    width=image.width,
                    num_frames=num_frames,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                )
            
            frames = output.frames[0]
            
            # Export to video file and return path
            video_file_path = self._export_video_to_file(frames, fps)
            
            logger.info("Video generation completed successfully")
            return video_file_path
            
        except Exception as e:
            logger.error(f"Error in video generation: {str(e)}")
            raise
    
    def _prepare_image_dimensions(self, image: Image.Image, pipeline) -> Image.Image:
        """Prepare image dimensions for video generation."""
        try:
            # Calculate optimal dimensions
            max_area = MAX_AREA_480P
            aspect_ratio = image.height / image.width
            mod_value = pipeline.vae_scale_factor_spatial * pipeline.transformer.config.patch_size[1]
            
            height = round(np.sqrt(max_area * aspect_ratio)) // mod_value * mod_value
            width = round(np.sqrt(max_area / aspect_ratio)) // mod_value * mod_value
            
            # Resize image
            resized_image = image.resize((width, height))
            logger.info(f"Resized image to {width}x{height}")
            
            return resized_image
            
        except Exception as e:
            logger.error(f"Error preparing image dimensions: {str(e)}")
            raise
    
    def _export_video_to_file(self, frames, fps: int) -> str:
        """Export video frames to file and return file path."""
        try:
            # Create unique filename
            video_filename = f"video_{uuid.uuid4().hex}.mp4"
            video_file_path = Path(TEMP_VIDEO_DIR) / video_filename
            
            # Export frames to video
            export_to_video(frames, str(video_file_path), fps=fps)
            
            logger.info(f"Video exported to: {video_file_path}")
            return str(video_file_path)
            
        except Exception as e:
            logger.error(f"Error exporting video to file: {str(e)}")
            raise

# Global generator instance
video_generator = VideoGenerator()
