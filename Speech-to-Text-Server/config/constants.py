"""
Application constants for Whisper Speech-to-Text Service.
"""

# API Settings
APP_NAME = "Speech-to-Text API"
DESCRIPTION = "Transcribe audio files to text using Whisper model"
VERSION = "1.0.0"

# File Upload Configuration
MAX_FILE_SIZE_MB = 10
MAX_AUDIO_DURATION_SEC = 600

# Audio Processing Configuration
TARGET_SAMPLE_RATE = 16000
SUPPORTED_AUDIO_FORMATS = [".wav", ".mp3", ".flac", ".m4a", ".ogg"]
CHUNK_DURATION_SEC = 30

# Whisper Model Configuration
MODEL_NAME = "openai/whisper-tiny"
TASK = "transcribe"
LANGUAGE = "english"
MAX_NEW_TOKENS = 444

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

# Response Configuration
MAX_FILENAME_LENGTH = 255
