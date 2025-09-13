"""
Application constants for FLUX Text-to-Image Service.
"""

# API Settings
APP_NAME = "Text-to-Image API"
DESCRIPTION = "Generate images from text prompts using FLUX.1-schnell"
VERSION = "1.0.0"

# Model Configuration
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
MODEL_DTYPE = "bfloat16"

# Image Generation Defaults
DEFAULT_GUIDANCE_SCALE = 0.0
DEFAULT_NUM_INFERENCE_STEPS = 4
DEFAULT_MAX_SEQUENCE_LENGTH = 256
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024

# Image Generation Limits
MIN_WIDTH = 256
MAX_WIDTH = 2048
MIN_HEIGHT = 256
MAX_HEIGHT = 2048
MIN_INFERENCE_STEPS = 1
MAX_INFERENCE_STEPS = 50
MIN_GUIDANCE_SCALE = 0.0
MAX_GUIDANCE_SCALE = 20.0
MAX_SEQUENCE_LENGTH_LIMIT = 512

# Memory Configuration
HIGH_VRAM_THRESHOLD_GB = 16
ENABLE_CPU_OFFLOAD_THRESHOLD = 16 * 1024**3  # 16GB in bytes

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

# Response Configuration
MAX_PROMPT_LENGTH = 2000
IMAGE_FORMAT = "PNG"
IMAGE_QUALITY = 95
