"""
Image-to-video generation API endpoints with file upload/download.
"""

import logging
import time
import tempfile
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from PIL import Image
import io
from typing import Optional  # Add this line

from core.generator import video_generator
from core.validation import validator
from config.constants import TEMP_VIDEO_DIR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["video"])

@router.post("/generate")
async def generate_video(
    image_file: UploadFile = File(..., description="Image file to generate video from"),
    prompt: str = Form(..., description="Text prompt for video generation"),
    negative_prompt: Optional[str] = Form(default="", description="Negative text prompt"),
    num_frames: int = Form(default=81, description="Number of frames to generate"),
    guidance_scale: float = Form(default=5.0, description="Guidance scale for generation"),
    fps: int = Form(default=16, description="Frames per second for output video")
) -> FileResponse:
    """Generate video from uploaded image file and return video file."""
    
    start_time = time.time()
    
    try:
        logger.info(f"Received video generation request for file: {image_file.filename}")
        
        # Validate uploaded image file
        validator.validate_image_file(image_file)
        
        # Read and process image file
        try:
            contents = await image_file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
        except Exception as e:
            logger.error(f"Failed to process image file: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Validate generation parameters
        validator.validate_generation_params(num_frames, guidance_scale, fps)
        
        # Generate video and get file path
        video_file_path = await video_generator.generate_video_from_image(
            image=image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_frames=num_frames,
            guidance_scale=guidance_scale,
            fps=fps
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Video generated successfully in {processing_time:.2f}s")
        
        # Generate unique filename for download
        original_name = Path(image_file.filename).stem if image_file.filename else "image"
        download_filename = f"{original_name}_generated_video_{int(time.time())}.mp4"

        background_tasks = BackgroundTasks()
        background_tasks.add_task(cleanup_file, video_file_path)
        
        # Return video file directly with cleanup
        return FileResponse(
            path=video_file_path,
            media_type="video/mp4",
            filename=download_filename,
            background=background_tasks
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during video generation")

def cleanup_file(file_path: str):
    """Clean up temporary video file after response is sent."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file {file_path}: {e}")
