"""
Request and response models for the Wan Image-to-Video API.
"""

from pydantic import BaseModel, Field
from typing import Optional

# Remove the VideoGenerationRequest class since we'll handle file uploads directly
# The request will now be handled as form data with UploadFile

class VideoGenerationMetadata(BaseModel):
    """Metadata for video generation response."""
    
    model_name: str = Field(..., description="Model used for generation")
    processing_time: float = Field(..., description="Time taken to generate the video")
    num_frames: int = Field(..., description="Number of frames generated")
    fps: int = Field(..., description="Frames per second")
    video_duration: float = Field(..., description="Video duration in seconds")
