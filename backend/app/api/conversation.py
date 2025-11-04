"""
Conversation API endpoints
대화 세션 관리 및 LLM 응답 생성
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.services.llm_service import llm_service
from app.services.stt_service import stt_service
from app.services.tts_service import tts_service

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ConversationRequest(BaseModel):
    user_input: str
    conversation_history: List[Message] = []
    scenario: str = "general"
    language: str = "Khmer"


class VoiceConversationRequest(BaseModel):
    conversation_history: List[Dict[str, str]] = []
    scenario: str = "general"
    language_code: str = "km-KH"


class EvaluationRequest(BaseModel):
    conversation_history: List[Message]
    learning_goals: Optional[List[str]] = None


@router.post("/send-message")
async def send_message(request: ConversationRequest):
    """
    텍스트 메시지 전송 및 AI 응답 받기

    - **user_input**: 사용자 입력 (크메르어)
    - **conversation_history**: 대화 기록
    - **scenario**: 시나리오 (market, transport, workplace, general)
    """
    try:
        # Convert Message objects to dicts
        context = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

        # Generate AI response
        response = await llm_service.generate_response(
            user_input=request.user_input,
            conversation_context=context,
            scenario=request.scenario,
            language=request.language,
        )

        return {
            "success": True,
            "data": response,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice-conversation")
async def voice_conversation(
    audio: UploadFile = File(...),
    scenario: str = "general",
    language_code: str = "km-KH",
):
    """
    음성 대화 - 음성을 받아서 텍스트 응답과 음성 응답을 모두 반환

    Complete voice conversation flow:
    1. User speaks (audio input)
    2. STT: Convert to text
    3. LLM: Generate response
    4. Return both text and audio response
    """
    try:
        # Step 1: Transcribe user's speech
        audio_content = await audio.read()
        transcription = await stt_service.transcribe_audio(
            audio_content=audio_content,
            language_code=language_code,
        )

        if not transcription["transcript"]:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in audio",
            )

        user_text = transcription["transcript"]

        # Step 2: Generate AI response
        ai_response = await llm_service.generate_response(
            user_input=user_text,
            conversation_context=[],  # Can be extended to include history
            scenario=scenario,
            language=_get_language_name(language_code),
        )

        # Step 3: Convert AI response to speech
        response_text = ai_response.get("response_text", "")
        audio_response = await tts_service.synthesize_speech(
            text=response_text,
            language_code=language_code,
        )

        # Encode audio as base64 for JSON response
        import base64
        audio_base64 = base64.b64encode(audio_response).decode('utf-8')

        return {
            "success": True,
            "data": {
                "user_input": {
                    "transcript": user_text,
                    "confidence": transcription["confidence"],
                },
                "ai_response": {
                    "text": response_text,
                    "translation_kr": ai_response.get("response_translation_kr", ""),
                    "key_phrases": ai_response.get("key_phrases", []),
                    "cultural_note": ai_response.get("cultural_note", ""),
                    "audio": audio_base64,  # Base64 encoded MP3
                },
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate")
async def evaluate_conversation(request: EvaluationRequest):
    """
    대화 세션 평가

    - **conversation_history**: 전체 대화 기록
    - **learning_goals**: 학습 목표 (선택)
    """
    try:
        # Convert Message objects to dicts
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

        # Evaluate conversation
        evaluation = await llm_service.evaluate_conversation(
            conversation_history=history,
            learning_goals=request.learning_goals,
        )

        return {
            "success": True,
            "data": evaluation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-text")
async def analyze_text(
    text: str,
    expected_text: Optional[str] = None,
    language: str = "Khmer",
):
    """
    텍스트 분석 (문법, 자연스러움 등)

    - **text**: 분석할 텍스트
    - **expected_text**: 예상 텍스트 (선택)
    """
    try:
        analysis = await llm_service.analyze_pronunciation(
            user_text=text,
            expected_text=expected_text,
            language=language,
        )

        return {
            "success": True,
            "data": analysis,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_language_name(language_code: str) -> str:
    """Map language code to language name"""
    language_map = {
        "km-KH": "Khmer",
        "lo-LA": "Lao",
        "vi-VN": "Vietnamese",
    }
    return language_map.get(language_code, "Khmer")
