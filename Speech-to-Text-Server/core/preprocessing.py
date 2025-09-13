"""
Audio preprocessing utilities for speech-to-text processing.
"""
import logging
import numpy as np
from scipy.signal import resample
from typing import List, Tuple

from config.constants import TARGET_SAMPLE_RATE, CHUNK_DURATION_SEC

logger = logging.getLogger(__name__)

class AudioPreprocessor:
    """Handles audio preprocessing operations."""
    
    @staticmethod
    def resample_audio_if_needed(audio_data: np.ndarray, original_sr: int, target_sr: int = TARGET_SAMPLE_RATE) -> Tuple[np.ndarray, int]:
        """
        Resample audio data to the target sample rate if original sample rate differs.

        Args:
            audio_data: The original audio signal data
            original_sr: The original sample rate of the audio data
            target_sr: The desired sample rate. Defaults to TARGET_SAMPLE_RATE

        Returns:
            Tuple of resampled audio data and target sample rate
        """
        if original_sr != target_sr:
            number_of_samples = round(len(audio_data) * float(target_sr) / original_sr)
            audio_data = resample(audio_data, number_of_samples)
            logger.info(f"Resampling from {original_sr} Hz to {target_sr} Hz")
        return audio_data, target_sr

    @staticmethod
    def convert_stereo_to_mono_if_needed(audio_data: np.ndarray) -> np.ndarray:
        """
        Convert stereo audio to mono by averaging channels if audio is stereo.

        Args:
            audio_data: The input audio data

        Returns:
            Mono audio data
        """
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
            logger.info('Converting stereo to mono')
        return audio_data

    @staticmethod
    def chunk_audio(audio_array: np.ndarray, sample_rate: int, chunk_duration_sec: int = CHUNK_DURATION_SEC) -> List[np.ndarray]:
        """
        Split audio into chunks of specified duration.

        Args:
            audio_array: The input audio array
            sample_rate: The sample rate of the audio
            chunk_duration_sec: Duration of each chunk in seconds

        Returns:
            List of audio chunks
        """
        chunk_size = int(chunk_duration_sec * sample_rate)
        chunks = [audio_array[i:i + chunk_size] for i in range(0, len(audio_array), chunk_size)]
        logger.info(f"Split audio into {len(chunks)} chunks of {chunk_duration_sec} seconds each")
        return chunks

    def preprocess_audio(self, audio_data: np.ndarray, sample_rate: int) -> Tuple[np.ndarray, int]:
        """
        Complete audio preprocessing pipeline.

        Args:
            audio_data: Raw audio data
            sample_rate: Original sample rate

        Returns:
            Tuple of processed audio data and final sample rate
        """
        # Resample if needed
        audio_data, sample_rate = self.resample_audio_if_needed(audio_data, sample_rate)
        
        # Convert to mono if needed
        audio_data = self.convert_stereo_to_mono_if_needed(audio_data)
        
        # Ensure mono (additional safety check)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        logger.info("Audio preprocessing completed")
        return audio_data, sample_rate

# Global preprocessor instance
preprocessor = AudioPreprocessor()
