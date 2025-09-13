"""
Image generation API endpoints.
"""
import time
import logging
from fastapi import APIRouter, HTTPException, Response

from api.models.requests import ImageRequest
from core.generator import generator
from core.validation import validator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["generation"])

@router.post("/imagine")
def generate_image_file(request: ImageRequest) -> Response:
    """
    Generate an image from text prompt and return as file download.
    
    Args:
        request: Image generation request parameters
        
    Returns:
        Response: PNG image file for download
    """
    # Validate request
    validator.validate_request(
        prompt=request.prompt,
        width=request.width,
        height=request.height,
        num_inference_steps=request.num_inference_steps,
        guidance_scale=request.guidance_scale,
        max_sequence_length=request.max_sequence_length,
        seed=request.seed
    )
    
    try:
        # Generate image (runs in thread pool automatically)
        image, seed, generation_time = generator.generate_image(
            prompt=request.prompt,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps,
            max_sequence_length=request.max_sequence_length,
            seed=request.seed,
            width=request.width,
            height=request.height
        )
        
        # Convert image to bytes
        image_bytes = generator.image_to_bytes(image)
        
        # Create filename
        filename = f"generated_image_{seed}_{int(time.time())}.png"
        
        # Return image as file download
        return Response(
            content=image_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(image_bytes)),
                "X-Generation-Time": str(generation_time),
                "X-Seed-Used": str(seed)
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Image generation endpoint failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )
