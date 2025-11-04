"""
Pronunciation Evaluation Service
STT와 LLM을 결합하여 발음 평가
"""
from app.services.stt_service import stt_service
from app.services.llm_service import llm_service
import logging
from typing import Dict, Any, Optional
import difflib

logger = logging.getLogger(__name__)


class PronunciationService:
    """Service for evaluating pronunciation quality"""

    def __init__(self):
        """Initialize pronunciation service"""
        self.stt = stt_service
        self.llm = llm_service
        logger.info("Pronunciation Service initialized")

    async def evaluate_pronunciation(
        self,
        audio_content: bytes,
        expected_text: Optional[str] = None,
        language_code: str = "km-KH",
    ) -> Dict[str, Any]:
        """
        Comprehensive pronunciation evaluation

        Args:
            audio_content: User's audio recording
            expected_text: What the user was supposed to say (optional)
            language_code: Language code

        Returns:
            Detailed pronunciation evaluation
        """
        try:
            # Step 1: Transcribe audio with alternatives
            transcription = await self.stt.transcribe_audio(
                audio_content=audio_content,
                language_code=language_code,
                enable_word_time_offsets=True,
            )

            if not transcription["transcript"]:
                return {
                    "error": "No speech detected",
                    "overall_score": 0,
                    "feedback": "음성이 감지되지 않았습니다. 다시 시도해주세요.",
                }

            user_text = transcription["transcript"]
            stt_confidence = transcription["confidence"]

            # Step 2: Calculate similarity if expected text is provided
            similarity_score = 100.0
            if expected_text:
                similarity_score = self._calculate_text_similarity(user_text, expected_text)

            # Step 3: Analyze word-level pronunciation
            word_scores = self._analyze_word_confidence(transcription.get("words", []))

            # Step 4: Get LLM feedback
            llm_analysis = await self.llm.analyze_pronunciation(
                user_text=user_text,
                expected_text=expected_text,
                language=self._get_language_name(language_code),
            )

            # Step 5: Calculate composite scores
            pronunciation_score = self._calculate_pronunciation_score(
                stt_confidence=stt_confidence,
                similarity_score=similarity_score,
                word_scores=word_scores,
            )

            return {
                "overall_score": pronunciation_score,
                "stt_confidence": round(stt_confidence * 100, 1),
                "similarity_score": round(similarity_score, 1),
                "transcription": user_text,
                "expected_text": expected_text or "",
                "word_analysis": word_scores,
                "llm_feedback": llm_analysis,
                "pronunciation_feedback": llm_analysis.get("pronunciation_feedback", ""),
                "suggestions": llm_analysis.get("suggestions", []),
                "grade": self._get_grade(pronunciation_score),
            }

        except Exception as e:
            logger.error(f"Pronunciation evaluation error: {e}")
            raise Exception(f"Failed to evaluate pronunciation: {str(e)}")

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using sequence matching

        Returns similarity score 0-100
        """
        if not text1 or not text2:
            return 0.0

        # Use SequenceMatcher for similarity
        similarity = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        return similarity * 100

    def _analyze_word_confidence(self, words: list) -> list:
        """
        Analyze confidence for each word

        Returns list of words with their confidence scores
        """
        word_analysis = []
        for word in words:
            confidence = word.get("confidence", 0.0)
            word_analysis.append({
                "word": word.get("word", ""),
                "confidence": round(confidence * 100, 1),
                "start_time": word.get("start_time", 0.0),
                "end_time": word.get("end_time", 0.0),
                "needs_practice": confidence < 0.7,  # Flag words with low confidence
            })

        return word_analysis

    def _calculate_pronunciation_score(
        self,
        stt_confidence: float,
        similarity_score: float,
        word_scores: list,
    ) -> float:
        """
        Calculate overall pronunciation score from multiple factors

        Weights:
        - STT confidence: 40%
        - Text similarity: 30%
        - Average word confidence: 30%
        """
        # STT confidence (0-1) -> 0-100
        stt_score = stt_confidence * 100

        # Average word confidence
        if word_scores:
            avg_word_confidence = sum(w["confidence"] for w in word_scores) / len(word_scores)
        else:
            avg_word_confidence = stt_score

        # Weighted average
        overall_score = (
            stt_score * 0.4 +
            similarity_score * 0.3 +
            avg_word_confidence * 0.3
        )

        return round(overall_score, 1)

    def _get_grade(self, score: float) -> str:
        """
        Convert numeric score to letter grade with Korean description
        """
        if score >= 90:
            return "A - 매우 우수"
        elif score >= 80:
            return "B - 우수"
        elif score >= 70:
            return "C - 양호"
        elif score >= 60:
            return "D - 보통"
        else:
            return "F - 연습 필요"

    def _get_language_name(self, language_code: str) -> str:
        """Map language code to language name"""
        language_map = {
            "km-KH": "Khmer",
            "lo-LA": "Lao",
            "vi-VN": "Vietnamese",
        }
        return language_map.get(language_code, "Unknown")

    async def get_practice_recommendations(
        self,
        word_analysis: list,
        overall_score: float,
    ) -> Dict[str, Any]:
        """
        Generate personalized practice recommendations

        Args:
            word_analysis: Word-level analysis from evaluation
            overall_score: Overall pronunciation score

        Returns:
            Practice recommendations
        """
        # Find words that need practice
        difficult_words = [
            w for w in word_analysis
            if w.get("needs_practice", False)
        ]

        recommendations = {
            "focus_areas": [],
            "practice_words": [w["word"] for w in difficult_words[:5]],  # Top 5 difficult words
            "next_steps": [],
        }

        # Recommendations based on score
        if overall_score < 60:
            recommendations["focus_areas"] = [
                "기본 발음 연습",
                "천천히 말하기 연습",
                "원어민 발음 듣고 따라하기",
            ]
            recommendations["next_steps"] = [
                "매일 10분씩 발음 연습하기",
                "간단한 인사말부터 시작하기",
            ]
        elif overall_score < 80:
            recommendations["focus_areas"] = [
                "억양과 리듬 개선",
                "어려운 단어 집중 연습",
            ]
            recommendations["next_steps"] = [
                "실제 대화 상황에서 연습하기",
                "어려운 단어 반복 연습하기",
            ]
        else:
            recommendations["focus_areas"] = [
                "자연스러운 회화 속도",
                "문화적 맥락 이해",
            ]
            recommendations["next_steps"] = [
                "현지인과 실제 대화하기",
                "다양한 상황에서 연습하기",
            ]

        return recommendations


# Global service instance
pronunciation_service = PronunciationService()
