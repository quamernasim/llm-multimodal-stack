"""
Input validation utilities for TTS requests.
"""
from fastapi import HTTPException
from config.constants import VALID_VOICES, MAX_TEXT_LENGTH

class RequestValidator:
    """Validates TTS requests."""
    
    @staticmethod
    def validate_text(text: str) -> None:
        """Validate input text."""
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        if len(text) > MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum length is {MAX_TEXT_LENGTH} characters"
            )
    
    @staticmethod
    def validate_voice(voice: str) -> None:
        """Validate voice selection."""
        if voice not in VALID_VOICES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice '{voice}'. Choose from: {', '.join(VALID_VOICES)}"
            )

# Global validator instance
validator = RequestValidator()
