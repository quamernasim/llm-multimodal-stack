"""
Request and response models for the API.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from config.constants import (
    DEFAULT_GUIDANCE_SCALE, DEFAULT_NUM_INFERENCE_STEPS, 
    DEFAULT_MAX_SEQUENCE_LENGTH, DEFAULT_WIDTH, DEFAULT_HEIGHT
)

class ImageRequest(BaseModel):
    """Request model for image generation."""
    prompt: str = Field(..., description="Text prompt for image generation")
    guidance_scale: float = Field(
        default=DEFAULT_GUIDANCE_SCALE, 
        description="How closely to follow the prompt"
    )
    num_inference_steps: int = Field(
        default=DEFAULT_NUM_INFERENCE_STEPS, 
        description="Number of denoising steps"
    )
    max_sequence_length: int = Field(
        default=DEFAULT_MAX_SEQUENCE_LENGTH, 
        description="Maximum sequence length for text encoding"
    )
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    width: int = Field(default=DEFAULT_WIDTH, description="Output image width")
    height: int = Field(default=DEFAULT_HEIGHT, description="Output image height")
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "A beautiful sunset over mountains with vibrant colors",
                "guidance_scale": 0.0,
                "num_inference_steps": 4,
                "max_sequence_length": 256,
                "seed": 42,
                "width": 1024,
                "height": 1024
            }
        }

class ImageResponse(BaseModel):
    """Response model for image generation."""
    image_base64: str = Field(..., description="Generated image encoded in base64")
    prompt: str = Field(..., description="Original prompt used")
    seed: int = Field(..., description="Seed used for generation")
    generation_time: float = Field(..., description="Time taken to generate image")
    metadata: Dict[str, Any] = Field(..., description="Additional generation metadata")

class HealthResponse(BaseModel):
    """Response model for health endpoint."""
    status: str
    service: str
    model_name: str
    device: str
    cuda_available: bool
    cpu_offload_enabled: bool
    torch_version: str
    vram_gb: float
    model_initialized: bool
