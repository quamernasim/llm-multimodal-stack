"""
Speech transcription API endpoints.
"""
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from api.models.requests import TranscriptionResponse
from core.transcriber import transcriber

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["transcription"])

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)) -> JSONResponse:
    """
    Transcribe speech from uploaded audio file.
    
    Args:
        file: Audio file to transcribe
        
    Returns:
        JSON response with transcription
    """
    try:
        # Process audio file and get transcription
        transcription_text = await transcriber.process_audio_file(file)
        
        # Create response
        response_data = TranscriptionResponse(
            transcription=transcription_text,
            processing_info={
                "filename": file.filename,
                "content_type": file.content_type
            }
        )
        
        return JSONResponse(
            content=response_data.dict(),
            status_code=200
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Transcription endpoint failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )
