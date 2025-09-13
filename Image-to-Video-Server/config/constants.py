"""
Application constants for Wan Image-to-Video service.
"""

# Model configuration (fixed/immutable values)
MODEL_ID = "Wan-AI/Wan2.1-I2V-14B-480P-Diffusers"
MODEL_PRECISION = "bfloat16"
VAE_PRECISION = "float32"
IMAGE_ENCODER_PRECISION = "float32"

# Video generation defaults
DEFAULT_NUM_FRAMES = 81
DEFAULT_GUIDANCE_SCALE = 5.0
DEFAULT_FPS = 16
MAX_AREA_480P = 480 * 832
MAX_AREA_720P = 720 * 1280
DEFAULT_INFERENCE_STEPS = 10

# Generation parameters limits
MIN_NUM_FRAMES = 8 # 16 changes later
MAX_NUM_FRAMES = 128
MIN_GUIDANCE_SCALE = 1.0
MAX_GUIDANCE_SCALE = 20.0
MIN_FPS = 8
MAX_FPS = 30

# Image constraints
MAX_IMAGE_SIZE_MB = 10
SUPPORTED_IMAGE_FORMATS = {"JPEG", "PNG", "JPG", "WEBP"}

# API configuration
API_PREFIX = "/api/v1"

# Video output
OUTPUT_VIDEO_FORMAT = "mp4"
TEMP_VIDEO_DIR = "temp_videos"

# Default values for environment variables (used by settings.py)
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_MAX_CONCURRENT_GENERATIONS = 2
DEFAULT_GENERATION_TIMEOUT = 300
