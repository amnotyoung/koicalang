"""
Text-to-Speech Service using Google Cloud TTS API
텍스트를 크메르어 음성으로 변환
"""
from google.cloud import texttospeech
from app.core.config import settings
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-Speech service for converting text to natural audio"""

    def __init__(self):
        """Initialize Google Cloud TTS client"""
        try:
            self.client = texttospeech.TextToSpeechClient()
            logger.info("TTS Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS Service: {e}")
            self.client = None

    async def synthesize_speech(
        self,
        text: str,
        language_code: str = "km-KH",  # Khmer
        voice_gender: str = "NEUTRAL",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
    ) -> bytes:
        """
        Convert text to speech audio

        Args:
            text: Text to convert to speech
            language_code: Language code (km-KH for Khmer)
            voice_gender: Voice gender (NEUTRAL, MALE, FEMALE)
            speaking_rate: Speaking rate (0.25 to 4.0, 1.0 is normal)
            pitch: Pitch adjustment (-20.0 to 20.0, 0.0 is normal)

        Returns:
            Audio content in bytes (MP3 format)
        """
        if not self.client:
            raise RuntimeError("TTS Service not initialized")

        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Map voice gender string to enum
            gender_map = {
                "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
                "MALE": texttospeech.SsmlVoiceGender.MALE,
                "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
            }

            # Select the type of audio file and audio settings
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                pitch=pitch,
                effects_profile_id=["handset-class-device"],  # Optimize for mobile devices
            )

            # Try Khmer first, fallback to English if it fails
            try:
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    ssml_gender=gender_map.get(voice_gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL),
                )

                # Perform the text-to-speech request
                response = self.client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config,
                )

                logger.info(f"Successfully synthesized speech for text: {text[:50]}...")
                return response.audio_content

            except Exception as e:
                # If Khmer fails, fallback to English
                logger.warning(f"TTS failed for {language_code}, falling back to en-US: {e}")

                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
                )

                response = self.client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config,
                )

                logger.info(f"Successfully synthesized speech in English for text: {text[:50]}...")
                return response.audio_content

        except Exception as e:
            logger.error(f"TTS synthesis error: {e}")
            raise Exception(f"Failed to synthesize speech: {str(e)}")

    async def get_available_voices(self, language_code: str = "km-KH") -> list:
        """
        Get available voices for a specific language

        Args:
            language_code: Language code to get voices for

        Returns:
            List of available voices with their properties
        """
        if not self.client:
            raise RuntimeError("TTS Service not initialized")

        try:
            voices = self.client.list_voices(language_code=language_code)

            available_voices = []
            for voice in voices.voices:
                available_voices.append({
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate": voice.natural_sample_rate_hertz,
                })

            return available_voices

        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            raise Exception(f"Failed to get available voices: {str(e)}")

    async def synthesize_with_ssml(
        self,
        ssml_text: str,
        language_code: str = "km-KH",
    ) -> bytes:
        """
        Convert SSML text to speech for advanced control

        SSML allows control over pronunciation, emphasis, breaks, etc.

        Example SSML:
        <speak>
            ជំរាបសួរ <break time="500ms"/>
            <emphasis level="strong">សូមអរគុណ</emphasis>
        </speak>
        """
        if not self.client:
            raise RuntimeError("TTS Service not initialized")

        try:
            synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            return response.audio_content

        except Exception as e:
            logger.error(f"SSML synthesis error: {e}")
            raise Exception(f"Failed to synthesize SSML: {str(e)}")


# Global service instance
tts_service = TTSService()
