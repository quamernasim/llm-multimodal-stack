"""
Image captioning API endpoints.
"""

import logging
from fastapi import APIRouter, File, HTTPException, UploadFile, Form

from api.models.requests import CaptionResponse
from core.generator import caption_generator
from core.validation import validator
from config.constants import TEMPERATURE, DO_SAMPLE, MAX_NEW_TOKENS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["caption"])

@router.post("/caption", response_model=CaptionResponse)
async def generate_caption(
    file: UploadFile = File(..., description="Image file to generate caption for"),
) -> CaptionResponse:
    """Generate caption for uploaded image."""

    try:
        # Validate image file
        validator.validate_image_file(file)

        # Read file content
        contents = await file.read()

        # Validate file size
        await validator.validate_file_size(contents)

        # Validate generation parameters
        validator.validate_generation_params(MAX_NEW_TOKENS, TEMPERATURE)

        # Generate caption
        result = await caption_generator.generate_caption(
            image_content=contents,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            do_sample=DO_SAMPLE
        )

        return CaptionResponse(
            caption=result["caption"],
            model_name=result["model_name"],
            processing_time=result["processing_time"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during caption generation")