"""
Application constants for BLIP-2 Image-to-Text Service.
"""

# Model Configuration
MODEL_NAME = "Salesforce/blip2-flan-t5-xl-coco"
MODEL_PRECISION = "float16" # hard coded for now, can be changed later
MAX_NEW_TOKENS = 256
TEMPERATURE = 1.0
DO_SAMPLE = True

# Image Configuration
MAX_IMAGE_SIZE_MB = 10
SUPPORTED_IMAGE_FORMATS = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

