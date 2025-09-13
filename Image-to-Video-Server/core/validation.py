"""
Input validation utilities for Wan Image-to-Video service.
"""

from fastapi import HTTPException, UploadFile
from config.constants import (
    MIN_NUM_FRAMES, MAX_NUM_FRAMES,
    MIN_GUIDANCE_SCALE, MAX_GUIDANCE_SCALE,
    MIN_FPS, MAX_FPS,
    MAX_IMAGE_SIZE_MB, SUPPORTED_IMAGE_FORMATS
)
import logging

logger = logging.getLogger(__name__)

class Validator:
    """Handles input validation for video generation requests."""
    
    def validate_image_file(self, file: UploadFile) -> None:
        """Validate uploaded image file."""
        
        # Check if file was uploaded
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        # Check file extension
        file_extension = file.filename.split('.')[-1].upper()
        if file_extension not in SUPPORTED_IMAGE_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
            )
        
        # Check content type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Image file validation passed: {file.filename}")
    
    async def validate_file_size(self, contents: bytes) -> None:
        """Validate file size."""
        size_mb = len(contents) / (1024 * 1024)
        if size_mb > MAX_IMAGE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({size_mb:.1f}MB) exceeds maximum allowed size ({MAX_IMAGE_SIZE_MB}MB)"
            )
    
    def validate_generation_params(
        self,
        num_frames: int,
        guidance_scale: float,
        fps: int
    ) -> None:
        """Validate video generation parameters."""
        
        # Validate num_frames
        if not (MIN_NUM_FRAMES <= num_frames <= MAX_NUM_FRAMES):
            raise HTTPException(
                status_code=400,
                detail=f"num_frames must be between {MIN_NUM_FRAMES} and {MAX_NUM_FRAMES}"
            )
        
        # Validate guidance_scale
        if not (MIN_GUIDANCE_SCALE <= guidance_scale <= MAX_GUIDANCE_SCALE):
            raise HTTPException(
                status_code=400,
                detail=f"guidance_scale must be between {MIN_GUIDANCE_SCALE} and {MAX_GUIDANCE_SCALE}"
            )
        
        # Validate fps
        if not (MIN_FPS <= fps <= MAX_FPS):
            raise HTTPException(
                status_code=400,
                detail=f"fps must be between {MIN_FPS} and {MAX_FPS}"
            )
        
        logger.info("Generation parameters validated successfully")

# Global validator instance
validator = Validator()
