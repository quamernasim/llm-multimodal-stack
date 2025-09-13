"""
Core image captioning functionality.
"""

import io
import time
import torch
import logging
import asyncio
from typing import Dict, Any
from PIL import Image

from core.model import model_manager
from config.constants import MODEL_NAME, TEMPERATURE, DO_SAMPLE, MAX_NEW_TOKENS

logger = logging.getLogger(__name__)

class CaptionGenerator:
    """Handles image captioning operations."""

    def __init__(self):
        pass

    async def generate_caption(
        self, 
        image_content: bytes, 
        max_new_tokens: int = MAX_NEW_TOKENS,
        temperature: float = TEMPERATURE,
        do_sample: bool = DO_SAMPLE
    ) -> Dict[str, Any]:
        """
        Generate caption for an image.

        Args:
            image_content (bytes): The image file content
            max_new_tokens (int): Maximum number of tokens to generate
            temperature (float): Temperature for generation
            do_sample (bool): Whether to use sampling

        Returns:
            Dict[str, Any]: Caption result with metadata

        Raises:
            Exception: If caption generation fails
        """
        start_time = time.time()
        logger.info("Starting image caption generation")

        try:
            # Load and process image
            image = self._load_image(image_content)

            # Get model and processor
            model = model_manager.get_model()
            processor = model_manager.get_processor()

            # Prepare inputs
            inputs = processor(image, return_tensors="pt").to("cuda", torch.float16)

            # Generate caption
            caption = await self._generate_text(
                model, processor, inputs, max_new_tokens, temperature, do_sample
            )

            processing_time = time.time() - start_time

            logger.info(f"Successfully generated caption in {processing_time:.2f} seconds")

            return {
                "caption": caption,
                "model_name": MODEL_NAME,
                "processing_time": processing_time
            }

        except Exception as e:
            logger.error(f"Caption generation failed: {e}")
            raise

    def _load_image(self, image_content: bytes) -> Image.Image:
        """Load image from bytes."""
        try:
            image = Image.open(io.BytesIO(image_content)).convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            raise ValueError("Invalid image file")

    async def _generate_text(
        self, 
        model, 
        processor, 
        inputs, 
        max_new_tokens: int,
        temperature: float,
        do_sample: bool
    ) -> str:
        """Generate text using the model."""
        try:
            # Generate response
            generated_ids = await asyncio.to_thread(
                model.generate,
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample
            )

            # Decode response
            generated_text = processor.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0].strip()

            return generated_text

        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            raise

# Global generator instance
caption_generator = CaptionGenerator()