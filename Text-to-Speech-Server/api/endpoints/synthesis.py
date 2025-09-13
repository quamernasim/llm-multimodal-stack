"""
Speech synthesis API endpoints.
"""
from fastapi import APIRouter, HTTPException, Response
from api.models.requests import TTSRequest
from core.synthesis import synthesizer
from core.validation import validator

router = APIRouter(prefix="/api/v1", tags=["synthesis"])

@router.post("/synthesize/")
def synthesize_speech(request: TTSRequest) -> Response:
    """
    Synthesize speech from text.
    
    Args:
        request: The synthesis request containing text and voice
        
    Returns:
        Response: WAV audio file response
    """
    # Validate request
    validator.validate_text(request.text)
    validator.validate_voice(request.voice)
    
    try:
        # Generate speech audio
        audio_data = synthesizer.generate_speech(request.text, request.voice)
        
        # Return audio response
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={
                "Content-Disposition": 'attachment; filename="synthesized_speech.wav"',
                "Content-Length": str(len(audio_data))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech synthesis failed: {str(e)}"
        )
