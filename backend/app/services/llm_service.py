"""
LLM Service using Google Gemini API
크메르어 대화 분석 및 피드백 생성
"""
import google.generativeai as genai
from app.core.config import settings
import logging
from typing import Dict, Any, List, Optional
import json

logger = logging.getLogger(__name__)


class LLMService:
    """Language Learning Model service for conversation and feedback"""

    def __init__(self):
        """Initialize Gemini API"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("LLM Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM Service: {e}")
            self.model = None

    async def analyze_pronunciation(
        self,
        user_text: str,
        expected_text: Optional[str] = None,
        language: str = "Khmer",
    ) -> Dict[str, Any]:
        """
        Analyze user's pronunciation and provide feedback

        Args:
            user_text: What the user actually said (from STT)
            expected_text: What the user was trying to say (optional)
            language: Target language

        Returns:
            Analysis with scores and feedback
        """
        if not self.model:
            raise RuntimeError("LLM Service not initialized")

        try:
            prompt = f"""
You are a {language} language teacher helping Korean volunteers learn practical conversation skills.

Analyze this {language} speech:
User said: "{user_text}"
{f'Expected: "{expected_text}"' if expected_text else ''}

Provide a detailed analysis in JSON format:
{{
    "accuracy_score": 0-100,
    "pronunciation_feedback": "Clear, specific feedback in Korean",
    "grammar_feedback": "Grammar notes in Korean",
    "naturalness_score": 0-100,
    "suggestions": ["Practical improvement tips in Korean"],
    "correct_version": "Corrected {language} text if needed"
}}

Focus on practical communication, not academic perfection. Be encouraging but honest.
"""

            response = self.model.generate_content(prompt)
            result = json.loads(response.text)

            return result

        except json.JSONDecodeError:
            # Fallback if response is not JSON
            logger.warning("LLM response was not valid JSON, returning raw response")
            return {
                "accuracy_score": 50,
                "pronunciation_feedback": response.text,
                "grammar_feedback": "",
                "naturalness_score": 50,
                "suggestions": [],
                "correct_version": user_text,
            }
        except Exception as e:
            logger.error(f"LLM analysis error: {e}")
            raise Exception(f"Failed to analyze pronunciation: {str(e)}")

    async def generate_response(
        self,
        user_input: str,
        conversation_context: List[Dict[str, str]],
        scenario: str = "general",
        language: str = "Khmer",
    ) -> Dict[str, Any]:
        """
        Generate AI response in the conversation

        Args:
            user_input: User's input text (in target language)
            conversation_context: Previous conversation messages
            scenario: Current scenario (market, transport, workplace, etc.)
            language: Target language

        Returns:
            AI response with text and metadata
        """
        if not self.model:
            raise RuntimeError("LLM Service not initialized")

        try:
            # Build conversation history
            context_text = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_context[-5:]  # Last 5 messages
            ])

            scenario_prompts = {
                "market": "You are a market vendor in Cambodia. Use simple, practical Khmer. Focus on prices, products, and basic negotiation.",
                "transport": "You are a tuk-tuk driver in Cambodia. Use casual Khmer for directions, prices, and small talk.",
                "workplace": "You are a Cambodian colleague at work. Use polite Khmer with appropriate honorifics.",
                "general": "You are a friendly Cambodian local helping a Korean volunteer practice Khmer.",
            }

            scenario_instruction = scenario_prompts.get(scenario, scenario_prompts["general"])

            prompt = f"""
{scenario_instruction}

Previous conversation:
{context_text}

User just said: "{user_input}"

Generate a natural response in {language} that:
1. Continues the conversation naturally
2. Uses vocabulary appropriate for the scenario
3. Keeps responses short and conversational (1-2 sentences)
4. Helps the learner practice practical phrases

Respond in JSON format:
{{
    "response_text": "Your {language} response",
    "response_translation_kr": "한국어 번역",
    "key_phrases": ["Important phrases from your response with Korean translation"],
    "cultural_note": "Optional cultural tip in Korean"
}}
"""

            response = self.model.generate_content(prompt)
            result = json.loads(response.text)

            return result

        except json.JSONDecodeError:
            logger.warning("LLM response was not valid JSON")
            return {
                "response_text": "សូមអភ័យទោស (Som aphey tos - Sorry)",
                "response_translation_kr": "죄송합니다",
                "key_phrases": [],
                "cultural_note": "",
            }
        except Exception as e:
            logger.error(f"LLM response generation error: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")

    async def evaluate_conversation(
        self,
        conversation_history: List[Dict[str, str]],
        learning_goals: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate overall conversation performance

        Args:
            conversation_history: Full conversation history
            learning_goals: Specific learning objectives (optional)

        Returns:
            Comprehensive evaluation with scores and recommendations
        """
        if not self.model:
            raise RuntimeError("LLM Service not initialized")

        try:
            conversation_text = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history
            ])

            goals_text = f"\nLearning goals: {', '.join(learning_goals)}" if learning_goals else ""

            prompt = f"""
You are evaluating a Korean volunteer's Khmer language practice session.

Conversation:
{conversation_text}
{goals_text}

Provide a comprehensive evaluation in JSON format:
{{
    "overall_score": 0-100,
    "fluency_score": 0-100,
    "vocabulary_score": 0-100,
    "grammar_score": 0-100,
    "strengths": ["List strengths in Korean"],
    "areas_for_improvement": ["List areas to work on in Korean"],
    "recommended_next_steps": ["Specific practice recommendations in Korean"],
    "encouraging_message": "Motivational message in Korean"
}}

Be constructive and encouraging. Focus on practical progress.
"""

            response = self.model.generate_content(prompt)
            result = json.loads(response.text)

            return result

        except json.JSONDecodeError:
            logger.warning("LLM evaluation response was not valid JSON")
            return {
                "overall_score": 70,
                "fluency_score": 70,
                "vocabulary_score": 70,
                "grammar_score": 70,
                "strengths": ["계속 연습하고 계십니다"],
                "areas_for_improvement": ["더 많은 연습이 필요합니다"],
                "recommended_next_steps": ["매일 대화 연습을 하세요"],
                "encouraging_message": "잘하고 계십니다! 계속 노력하세요!",
            }
        except Exception as e:
            logger.error(f"LLM evaluation error: {e}")
            raise Exception(f"Failed to evaluate conversation: {str(e)}")


# Global service instance
llm_service = LLMService()
