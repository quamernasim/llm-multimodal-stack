"""
Application constants for Orpheus TTS Service.
"""

# Audio Configuration
SAMPLE_RATE = 24000
AUDIO_FORMAT = "WAV"
AUDIO_SUBTYPE = "PCM_16"

# Model Configuration
MODEL_NAME = "canopylabs/orpheus-tts-0.1-finetune-prod"
MAX_MODEL_LENGTH = 10000
GPU_MEMORY_UTILIZATION = 0.4
MAX_NUM_SEQUENCES = 1
MAX_AUDIO_TOKENS = 10000 # logs-    83 tokens per second

# Voice Configuration
VALID_VOICES = ["tara", "leah", "jess", "leo", "dan", "mia", "zac"]

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

# Response Configuration
MAX_TEXT_LENGTH = 5000
