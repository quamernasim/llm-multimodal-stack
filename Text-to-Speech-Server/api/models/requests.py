"""
Request and response models for the API.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TTSRequest(BaseModel):
    """Request model for text-to-speech synthesis."""
    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field(default="tara", description="Voice to use for synthesis")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, this is a test of the text-to-speech system.",
                "voice": "tara"
            }
        }

class VoiceInfo(BaseModel):
    """Voice information model."""
    name: str
    description: str

class VoicesResponse(BaseModel):
    """Response model for voices endpoint."""
    voices: List[VoiceInfo]
