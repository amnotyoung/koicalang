"""
Speech-to-Text Service using Google Cloud Speech API
크메르어 음성을 텍스트로 변환
"""
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
from app.core.config import settings
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class STTService:
    """Speech-to-Text service for converting audio to text"""

    def __init__(self):
        """Initialize Google Cloud Speech client"""
        try:
            self.client = speech.SpeechClient()
            logger.info("STT Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize STT Service: {e}")
            self.client = None

    async def transcribe_audio(
        self,
        audio_content: bytes,
        language_code: str = "km-KH",  # Khmer (Cambodia)
        sample_rate: int = None,
        enable_word_time_offsets: bool = True,
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text with pronunciation details

        Args:
            audio_content: Audio file content in bytes
            language_code: Language code (km-KH for Khmer, lo-LA for Lao, vi-VN for Vietnamese)
            sample_rate: Audio sample rate in Hz (None for auto-detect)
            enable_word_time_offsets: Whether to include word-level timestamps

        Returns:
            Dictionary containing:
            - transcript: The recognized text
            - confidence: Recognition confidence (0-1)
            - words: List of words with timing and confidence
        """
        if not self.client:
            raise RuntimeError("STT Service not initialized")

        try:
            # Configure recognition settings - let Google auto-detect encoding and sample rate
            config = RecognitionConfig(
                encoding=RecognitionConfig.AudioEncoding.WEBM_OPUS,
                language_code=language_code,
                enable_word_time_offsets=enable_word_time_offsets,
                enable_automatic_punctuation=True,
                model="default",  # Use 'latest_long' for better accuracy on longer audio
            )

            audio = RecognitionAudio(content=audio_content)

            # Perform recognition
            response = self.client.recognize(config=config, audio=audio)

            if not response.results:
                return {
                    "transcript": "",
                    "confidence": 0.0,
                    "words": [],
                    "message": "No speech detected",
                }

            # Get the first result (highest confidence)
            result = response.results[0]
            alternative = result.alternatives[0]

            # Extract word-level details
            words = []
            if enable_word_time_offsets and hasattr(alternative, "words"):
                for word_info in alternative.words:
                    words.append({
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                        "confidence": getattr(word_info, "confidence", alternative.confidence),
                    })

            return {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence,
                "words": words,
                "language": language_code,
            }

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")

    async def transcribe_with_alternatives(
        self,
        audio_content: bytes,
        language_code: str = "km-KH",
        max_alternatives: int = 3,
    ) -> Dict[str, Any]:
        """
        Transcribe audio and return multiple alternatives

        Useful for pronunciation evaluation to compare different interpretations
        """
        if not self.client:
            raise RuntimeError("STT Service not initialized")

        try:
            config = RecognitionConfig(
                encoding=RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=settings.AUDIO_SAMPLE_RATE,
                language_code=language_code,
                max_alternatives=max_alternatives,
                enable_word_confidence=True,
            )

            audio = RecognitionAudio(content=audio_content)
            response = self.client.recognize(config=config, audio=audio)

            if not response.results:
                return {"alternatives": [], "message": "No speech detected"}

            result = response.results[0]
            alternatives = []

            for alternative in result.alternatives:
                alternatives.append({
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence,
                })

            return {
                "alternatives": alternatives,
                "language": language_code,
            }

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")


# Global service instance
stt_service = STTService()
