"""
Core speech synthesis functionality.
"""
import io
import time
import logging
import numpy as np
import soundfile as sf
from typing import Generator

from config.constants import SAMPLE_RATE, AUDIO_FORMAT, AUDIO_SUBTYPE, MAX_AUDIO_TOKENS
from core.model import model_manager

logger = logging.getLogger(__name__)

class SpeechSynthesizer:
    """Handles speech synthesis operations."""
    
    def generate_speech(self, text: str, voice: str) -> bytes:
        """
        Generate speech audio from text using the Orpheus TTS model.
        
        Args:
            text (str): The input text to synthesize
            voice (str): The voice to use for synthesis
            
        Returns:
            bytes: WAV audio data
            
        Raises:
            Exception: If synthesis fails
        """
        start_time = time.time()
        logger.info(f"Starting speech synthesis for text: '{text[:50]}...' with voice: {voice}")
        
        try:
            model = model_manager.get_model()
            
            # Generate speech tokens
            syn_tokens = model.generate_speech(
                prompt=text,
                voice=voice,
                max_tokens=MAX_AUDIO_TOKENS,
            )
            
            # Process audio chunks
            audio_data = self._process_audio_chunks(syn_tokens)
            
            # Log synthesis metrics
            self._log_synthesis_metrics(audio_data, start_time)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            raise
    
    def _process_audio_chunks(self, syn_tokens: Generator) -> bytes:
        """Process audio chunks from the model into WAV format."""
        # Collect all audio chunks
        audio_chunks = []
        for audio_chunk in syn_tokens:
            audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
            audio_chunks.append(audio_array)
        
        if not audio_chunks:
            raise ValueError("No audio chunks generated")
        
        # Concatenate all audio chunks
        full_audio = np.concatenate(audio_chunks)
        
        # Create WAV file in memory
        audio_buffer = io.BytesIO()
        sf.write(
            audio_buffer,
            full_audio,
            SAMPLE_RATE,
            format=AUDIO_FORMAT,
            subtype=AUDIO_SUBTYPE
        )
        
        audio_buffer.seek(0)
        return audio_buffer.read()
    
    def _log_synthesis_metrics(self, audio_data: bytes, start_time: float) -> None:
        """Log synthesis performance metrics."""
        # Estimate audio duration (rough calculation)
        estimated_samples = len(audio_data) / 2  # 16-bit audio = 2 bytes per sample
        duration = estimated_samples / SAMPLE_RATE
        processing_time = time.time() - start_time
        rtf = processing_time / duration if duration > 0 else 0
        
        logger.info(
            f"Successfully generated {duration:.2f} seconds of audio "
            f"in {processing_time:.2f} seconds (RTF: {rtf:.2f})"
        )

# Global synthesizer instance
synthesizer = SpeechSynthesizer()
