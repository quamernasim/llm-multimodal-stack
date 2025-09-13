"""
Input validation utilities for image generation requests.
"""
import logging
from fastapi import HTTPException

from config.constants import (
    MAX_PROMPT_LENGTH, MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT,
    MIN_INFERENCE_STEPS, MAX_INFERENCE_STEPS, MIN_GUIDANCE_SCALE, 
    MAX_GUIDANCE_SCALE, MAX_SEQUENCE_LENGTH_LIMIT
)

logger = logging.getLogger(__name__)

class RequestValidator:
    """Validates image generation requests."""
    
    @staticmethod
    def validate_prompt(prompt: str) -> None:
        """Validate input prompt."""
        if not prompt or not prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )
        
        if len(prompt) > MAX_PROMPT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Prompt too long. Maximum length is {MAX_PROMPT_LENGTH} characters"
            )
    
    @staticmethod
    def validate_dimensions(width: int, height: int) -> None:
        """Validate image dimensions."""
        if not (MIN_WIDTH <= width <= MAX_WIDTH):
            raise HTTPException(
                status_code=400,
                detail=f"Width must be between {MIN_WIDTH} and {MAX_WIDTH} pixels"
            )
        
        if not (MIN_HEIGHT <= height <= MAX_HEIGHT):
            raise HTTPException(
                status_code=400,
                detail=f"Height must be between {MIN_HEIGHT} and {MAX_HEIGHT} pixels"
            )
        
        # Check if dimensions are multiples of 8 (common requirement for diffusion models)
        if width % 8 != 0 or height % 8 != 0:
            raise HTTPException(
                status_code=400,
                detail="Width and height must be multiples of 8"
            )
    
    @staticmethod
    def validate_inference_steps(num_inference_steps: int) -> None:
        """Validate number of inference steps."""
        if not (MIN_INFERENCE_STEPS <= num_inference_steps <= MAX_INFERENCE_STEPS):
            raise HTTPException(
                status_code=400,
                detail=f"Number of inference steps must be between {MIN_INFERENCE_STEPS} and {MAX_INFERENCE_STEPS}"
            )
    
    @staticmethod
    def validate_guidance_scale(guidance_scale: float) -> None:
        """Validate guidance scale."""
        if not (MIN_GUIDANCE_SCALE <= guidance_scale <= MAX_GUIDANCE_SCALE):
            raise HTTPException(
                status_code=400,
                detail=f"Guidance scale must be between {MIN_GUIDANCE_SCALE} and {MAX_GUIDANCE_SCALE}"
            )
    
    @staticmethod
    def validate_sequence_length(max_sequence_length: int) -> None:
        """Validate maximum sequence length."""
        if max_sequence_length <= 0 or max_sequence_length > MAX_SEQUENCE_LENGTH_LIMIT:
            raise HTTPException(
                status_code=400,
                detail=f"Max sequence length must be between 1 and {MAX_SEQUENCE_LENGTH_LIMIT}"
            )
    
    @staticmethod
    def validate_seed(seed: int) -> None:
        """Validate seed value."""
        if seed is not None and (seed < 0 or seed >= 2**32):
            raise HTTPException(
                status_code=400,
                detail="Seed must be between 0 and 2^32-1"
            )
    
    def validate_request(
        self,
        prompt: str,
        width: int,
        height: int,
        num_inference_steps: int,
        guidance_scale: float,
        max_sequence_length: int,
        seed: int = None
    ) -> None:
        """Validate complete image generation request."""
        self.validate_prompt(prompt)
        self.validate_dimensions(width, height)
        self.validate_inference_steps(num_inference_steps)
        self.validate_guidance_scale(guidance_scale)
        self.validate_sequence_length(max_sequence_length)
        if seed is not None:
            self.validate_seed(seed)
        
        logger.info("Request validation passed")

# Global validator instance
validator = RequestValidator()
