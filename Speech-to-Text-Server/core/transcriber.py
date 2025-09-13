"""
Core speech transcription functionality.
"""
import asyncio
import time
import logging
import numpy as np
import soundfile as sf
from typing import List
from fastapi import UploadFile

from core.model import model_manager
from core.preprocessing import preprocessor
from core.validation import validator
from config.constants import MAX_NEW_TOKENS, LANGUAGE, TASK

logger = logging.getLogger(__name__)

class SpeechTranscriber:
    """Handles speech transcription operations."""
    
    async def transcribe_audio_chunk(self, audio_array: np.ndarray, sampling_rate: int) -> str:
        """
        Transcribe a single audio chunk using the Whisper model.
        
        Args:
            audio_array: Audio data as numpy array
            sampling_rate: Sample rate of the audio
            
        Returns:
            Transcribed text
            
        Raises:
            Exception: If transcription fails
        """
        start_time = time.time()
        
        try:
            model, processor = model_manager.get_model_and_processor()
            device = model_manager.get_device()
            
            # Process audio features
            input_features = processor(
                audio_array, 
                sampling_rate=sampling_rate, 
                return_tensors="pt"
            ).input_features.to(device)

            # Get decoder prompt IDs
            forced_decoder_ids = processor.get_decoder_prompt_ids(
                language=LANGUAGE, 
                task=TASK
            )

            # Generate transcription
            predicted_ids = await asyncio.to_thread(
                model.generate,
                input_features,
                max_new_tokens=MAX_NEW_TOKENS,
                forced_decoder_ids=forced_decoder_ids,
            )

            # Decode the prediction
            text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            
            processing_time = time.time() - start_time
            logger.info(f"Chunk transcription completed in {processing_time:.2f} seconds")
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Transcription failed for audio chunk: {e}")
            raise

    async def process_audio_file(self, file: UploadFile) -> str:
        """
        Process an uploaded audio file and return transcription.
        
        Args:
            file: Uploaded audio file
            
        Returns:
            Complete transcription text
            
        Raises:
            HTTPException: If file processing fails
        """
        # Validate file
        await validator.validate_audio_file(file)
        
        try:
            # Read audio file
            file.file.seek(0)
            audio_data, sample_rate = await asyncio.to_thread(sf.read, file.file)
            
            # Validate audio duration
            validator.validate_audio_duration(audio_data, sample_rate)
            
            # Preprocess audio
            audio_data, sample_rate = preprocessor.preprocess_audio(audio_data, sample_rate)
            
            # Split into chunks
            audio_chunks = preprocessor.chunk_audio(audio_data, sample_rate)
            
            # Transcribe each chunk
            transcriptions = await self._transcribe_chunks(audio_chunks, sample_rate)
            
            # Combine transcriptions
            final_transcription = " ".join(transcriptions)
            
            logger.info(f"File transcription completed. Total chunks: {len(audio_chunks)}")
            return final_transcription
            
        except Exception as e:
            logger.error(f"Audio file processing failed: {e}")
            raise

    async def _transcribe_chunks(self, audio_chunks: List[np.ndarray], sample_rate: int) -> List[str]:
        """
        Transcribe multiple audio chunks.
        
        Args:
            audio_chunks: List of audio chunk arrays
            sample_rate: Sample rate of the audio
            
        Returns:
            List of transcription strings
        """
        transcriptions = []
        
        for idx, chunk in enumerate(audio_chunks):
            logger.info(f"Processing chunk {idx + 1}/{len(audio_chunks)}")
            
            try:
                text = await self.transcribe_audio_chunk(chunk, sample_rate)
                transcriptions.append(text)
            except Exception as e:
                logger.error(f"Error processing chunk {idx + 1}: {e}")
                transcriptions.append("[Error in chunk]")
        
        return transcriptions

# Global transcriber instance
transcriber = SpeechTranscriber()
