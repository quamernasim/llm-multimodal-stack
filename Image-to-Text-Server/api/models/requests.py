"""
Request and response models for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional

class CaptionResponse(BaseModel):
    """Response model for image captioning."""

    caption: str = Field(..., description="Generated caption for the image")
    model_name: str = Field(..., description="Model used for generation")
    processing_time: float = Field(..., description="Time taken to process the image")

    class Config:
        schema_extra = {
            "example": {
                "caption": "A beautiful sunset over the ocean",
                "model_name": "Salesforce/blip2-flan-t5-xl-coco",
                "processing_time": 2.34
            }
        }