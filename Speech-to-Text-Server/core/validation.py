"""
Input validation utilities for speech-to-text requests.
"""
import asyncio
import logging
from fastapi import HTTPException, UploadFile
import numpy as np

from config.constants import (
    MAX_FILE_SIZE_MB, SUPPORTED_AUDIO_FORMATS, 
    MAX_AUDIO_DURATION_SEC, MAX_FILENAME_LENGTH
)

logger = logging.getLogger(__name__)

class RequestValidator:
    """Validates speech-to-text requests."""
    
    async def validate_audio_file(self, file: UploadFile) -> None:
        """
        Validate uploaded audio file.
        
        Args:
            file: Uploaded file to validate
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )
        
        if len(file.filename) > MAX_FILENAME_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Filename too long. Maximum length is {MAX_FILENAME_LENGTH} characters"
            )
        
        # Validate file format
        if not file.filename.lower().endswith(tuple(SUPPORTED_AUDIO_FORMATS)):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Supported formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}"
            )
        
        # Validate file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds limit of {MAX_FILE_SIZE_MB}MB"
            )
        
        # Reset file position for later reading
        file.file.seek(0)
        
        logger.info(f"File validation passed for: {file.filename}")
    
    def validate_audio_duration(self, audio_data: np.ndarray, sample_rate: int) -> None:
        """
        Validate audio duration.
        
        Args:
            audio_data: Audio data array
            sample_rate: Sample rate of the audio
            
        Raises:
            HTTPException: If audio is too long
        """
        duration_seconds = len(audio_data) / sample_rate
        
        if duration_seconds > MAX_AUDIO_DURATION_SEC:
            raise HTTPException(
                status_code=400,
                detail=f"Audio too long. Maximum duration is {MAX_AUDIO_DURATION_SEC} seconds"
            )
        
        logger.info(f"Audio duration validation passed: {duration_seconds:.2f} seconds")

# Global validator instance
validator = RequestValidator()

