"""
Voice management API endpoints.
"""
from fastapi import APIRouter
from api.models.requests import VoicesResponse, VoiceInfo
from config.constants import VALID_VOICES

router = APIRouter(prefix="/api/v1", tags=["voices"])

@router.get("/voices", response_model=VoicesResponse)
async def list_voices() -> VoicesResponse:
    """Get list of available voices for synthesis."""
    voice_descriptions = {
        "tara": "Female voice",
        "leah": "Female voice", 
        "jess": "Female voice",
        "leo": "Male voice",
        "dan": "Male voice",
        "mia": "Female voice",
        "zac": "Male voice"
    }
    
    voices = [
        VoiceInfo(name=voice, description=voice_descriptions.get(voice, "Unknown"))
        for voice in VALID_VOICES
    ]
    
    return VoicesResponse(voices=voices)
