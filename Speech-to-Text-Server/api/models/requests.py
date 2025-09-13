"""
Request and response models for the API.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TranscriptionResponse(BaseModel):
    """Response model for transcription endpoint."""
    transcription: str = Field(..., description="Transcribed text from audio")
    processing_info: Optional[Dict[str, Any]] = Field(None, description="Additional processing information")

class HealthResponse(BaseModel):
    """Response model for health endpoint."""
    status: str
    service: str
    model_name: str
    device: str
    cuda_available: bool
    supported_formats: List[str]
    torch_version: str
    model_initialized: bool
