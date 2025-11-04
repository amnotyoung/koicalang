"""
Voice API endpoints
음성 녹음, STT, TTS, 발음 평가
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io

from app.services.stt_service import stt_service
from app.services.tts_service import tts_service
from app.services.pronunciation_service import pronunciation_service

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    language_code: str = "km-KH"
    voice_gender: str = "NEUTRAL"
    speaking_rate: float = 1.0


class PronunciationRequest(BaseModel):
    expected_text: Optional[str] = None
    language_code: str = "km-KH"


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language_code: str = "km-KH",
):
    """
    음성을 텍스트로 변환 (STT)

    - **audio**: 음성 파일 (WAV, MP3, etc.)
    - **language_code**: 언어 코드 (km-KH, lo-LA, vi-VN)
    """
    try:
        # Read audio file
        audio_content = await audio.read()

        # Transcribe
        result = await stt_service.transcribe_audio(
            audio_content=audio_content,
            language_code=language_code,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize")
async def synthesize_speech(request: TTSRequest):
    """
    텍스트를 음성으로 변환 (TTS)

    Returns audio file (MP3)
    """
    try:
        # Synthesize speech
        audio_content = await tts_service.synthesize_speech(
            text=request.text,
            language_code=request.language_code,
            voice_gender=request.voice_gender,
            speaking_rate=request.speaking_rate,
        )

        # Return as streaming audio
        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=speech.mp3"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate-pronunciation")
async def evaluate_pronunciation(
    audio: UploadFile = File(...),
    expected_text: Optional[str] = None,
    language_code: str = "km-KH",
):
    """
    발음 평가

    - **audio**: 사용자 음성 파일
    - **expected_text**: 예상 텍스트 (선택)
    - **language_code**: 언어 코드
    """
    try:
        # Read audio file
        audio_content = await audio.read()

        # Evaluate pronunciation
        result = await pronunciation_service.evaluate_pronunciation(
            audio_content=audio_content,
            expected_text=expected_text,
            language_code=language_code,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/voices")
async def get_available_voices(language_code: str = "km-KH"):
    """
    사용 가능한 음성 목록 조회
    """
    try:
        voices = await tts_service.get_available_voices(language_code=language_code)

        return {
            "success": True,
            "data": {
                "language_code": language_code,
                "voices": voices,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
