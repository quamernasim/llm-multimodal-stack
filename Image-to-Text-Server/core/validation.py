"""
Input validation utilities for image captioning requests.
"""

from fastapi import HTTPException, UploadFile
from config.constants import MAX_IMAGE_SIZE_MB, SUPPORTED_IMAGE_FORMATS

class RequestValidator:
    """Validates image captioning requests."""

    @staticmethod
    def validate_image_file(file: UploadFile) -> None:
        """Validate uploaded image file."""
        # Check content type
        if not file.content_type or file.content_type not in SUPPORTED_IMAGE_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format. Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
            )

    @staticmethod
    async def validate_file_size(contents: bytes) -> None:
        """Validate file size."""
        if len(contents) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
            )

    @staticmethod
    def validate_generation_params(max_new_tokens: int, temperature: float) -> None:
        """Validate generation parameters."""
        if max_new_tokens <= 0 or max_new_tokens > 1000:
            raise HTTPException(
                status_code=400,
                detail="max_new_tokens must be between 1 and 1000"
            )

        if temperature <= 0 or temperature > 2.0:
            raise HTTPException(
                status_code=400,
                detail="temperature must be between 0 and 2.0"
            )

# Global validator instance
validator = RequestValidator()