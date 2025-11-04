"""
Scenarios API endpoints
실전 대화 시나리오 (시장, 교통, 직장)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()


# 시나리오 데이터 정의
SCENARIOS = {
    "market": {
        "id": "market",
        "name_kr": "시장에서 장보기",
        "name_en": "Shopping at Market",
        "description": "현지 시장에서 물건을 사고, 가격을 흥정하고, 신선도를 확인하는 대화 연습",
        "difficulty": "beginner",
        "key_phrases": [
            {
                "khmer": "នេះថ្លៃប៉ុន្មាន?",
                "romanization": "Nih tlay ponmaan?",
                "korean": "이것 얼마예요?",
                "english": "How much is this?",
            },
            {
                "khmer": "សុំថោកបន្តិចបានទេ?",
                "romanization": "Som thaok bantich ban te?",
                "korean": "좀 깎아주실 수 있나요?",
                "english": "Can you give me a discount?",
            },
            {
                "khmer": "ស្រស់ទេ?",
                "romanization": "Sros te?",
                "korean": "신선한가요?",
                "english": "Is it fresh?",
            },
            {
                "khmer": "អរគុណ",
                "romanization": "Orkun",
                "korean": "감사합니다",
                "english": "Thank you",
            },
        ],
        "vocabulary": [
            {"khmer": "ថ្លៃ", "romanization": "tlay", "meaning": "비싸다/가격"},
            {"khmer": "ថោក", "romanization": "thaok", "meaning": "싸다"},
            {"khmer": "ស្រស់", "romanization": "sros", "meaning": "신선하다"},
            {"khmer": "ផ្លែឈើ", "romanization": "phlae chheu", "meaning": "과일"},
            {"khmer": "បន្លែ", "romanization": "bonlae", "meaning": "채소"},
        ],
        "conversation_starters": [
            "ជំរាបសួរ! អ្នកត្រូវការអ្វី?",  # Hello! What do you need?
            "មើលទៅមើលមក ទិញអ្វីខ្លះ?",  # Looking around, what are you buying?
        ],
    },
    "transport": {
        "id": "transport",
        "name_kr": "뚝뚝(툭툭) 이용 및 길 찾기",
        "name_en": "Using Tuk-Tuk / Getting Directions",
        "description": "뚝뚝을 타거나 길을 물어보는 실전 대화 연습",
        "difficulty": "beginner",
        "key_phrases": [
            {
                "khmer": "ទៅ... ប៉ុន្មាន?",
                "romanization": "Tov... ponmaan?",
                "korean": "...까지 얼마예요?",
                "english": "How much to...?",
            },
            {
                "khmer": "ឆ្ងាយប៉ុន្មាន?",
                "romanization": "Chhngaay ponmaan?",
                "korean": "얼마나 멀어요?",
                "english": "How far is it?",
            },
            {
                "khmer": "... នៅឯណា?",
                "romanization": "... nov ey na?",
                "korean": "...이/가 어디 있어요?",
                "english": "Where is...?",
            },
            {
                "khmer": "បត់ឆ្វេង/ស្ដាំ",
                "romanization": "bat chveng/sdam",
                "korean": "왼쪽/오른쪽으로 도세요",
                "english": "Turn left/right",
            },
        ],
        "vocabulary": [
            {"khmer": "ទៅ", "romanization": "tov", "meaning": "가다"},
            {"khmer": "ឆ្ងាយ", "romanization": "chhngaay", "meaning": "멀다"},
            {"khmer": "ជិត", "romanization": "chit", "meaning": "가깝다"},
            {"khmer": "ត្រង់", "romanization": "trong", "meaning": "직진"},
            {"khmer": "ឈប់", "romanization": "chhob", "meaning": "멈추다"},
        ],
        "conversation_starters": [
            "ទៅណា បង?",  # Where are you going?
            "តម្លៃ ២ ដុល្លារ អញ្ចឹង",  # The price is 2 dollars
        ],
    },
    "workplace": {
        "id": "workplace",
        "name_kr": "현지 동료/상사와 인사",
        "name_en": "Workplace Greetings",
        "description": "직장에서 동료 및 상사와 인사하고 간단한 업무 대화하기",
        "difficulty": "intermediate",
        "key_phrases": [
            {
                "khmer": "ជំរាបសួរ លោក/លោកស្រី",
                "romanization": "Chumreap suor lok/lok srey",
                "korean": "안녕하세요 (공손하게)",
                "english": "Hello (polite)",
            },
            {
                "khmer": "សុខសប្បាយទេ?",
                "romanization": "Sok sabbaay te?",
                "korean": "잘 지내세요?",
                "english": "How are you?",
            },
            {
                "khmer": "សុំជួយផង",
                "romanization": "Som chuoy phong",
                "korean": "도와주세요",
                "english": "Please help me",
            },
            {
                "khmer": "បាទ/ចាស",
                "romanization": "Baat/Chas",
                "korean": "네 (남성/여성)",
                "english": "Yes (male/female)",
            },
        ],
        "vocabulary": [
            {"khmer": "លោក", "romanization": "lok", "meaning": "선생님 (남성 존칭)"},
            {"khmer": "លោកស្រី", "romanization": "lok srey", "meaning": "선생님 (여성 존칭)"},
            {"khmer": "ការងារ", "romanization": "kar ngar", "meaning": "일/업무"},
            {"khmer": "ជួយ", "romanization": "chuoy", "meaning": "돕다"},
            {"khmer": "អរគុណច្រើន", "romanization": "orkun chraen", "meaning": "대단히 감사합니다"},
        ],
        "conversation_starters": [
            "ជំរាបសួរ! សុខសប្បាយទេ?",  # Hello! How are you?
            "ថ្ងៃនេះមានការងារច្រើនទេ?",  # Do you have a lot of work today?
        ],
    },
}


class ScenarioResponse(BaseModel):
    id: str
    name_kr: str
    name_en: str
    description: str
    difficulty: str


@router.get("/list")
async def list_scenarios() -> Dict[str, Any]:
    """
    사용 가능한 모든 시나리오 목록 반환
    """
    scenarios_list = [
        {
            "id": s["id"],
            "name_kr": s["name_kr"],
            "name_en": s["name_en"],
            "description": s["description"],
            "difficulty": s["difficulty"],
        }
        for s in SCENARIOS.values()
    ]

    return {
        "success": True,
        "data": {
            "scenarios": scenarios_list,
            "total": len(scenarios_list),
        },
    }


@router.get("/{scenario_id}")
async def get_scenario_details(scenario_id: str) -> Dict[str, Any]:
    """
    특정 시나리오의 상세 정보 반환

    - **scenario_id**: market, transport, workplace
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found",
        )

    scenario = SCENARIOS[scenario_id]

    return {
        "success": True,
        "data": scenario,
    }


@router.get("/{scenario_id}/phrases")
async def get_key_phrases(scenario_id: str) -> Dict[str, Any]:
    """
    시나리오별 핵심 표현 반환
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found",
        )

    scenario = SCENARIOS[scenario_id]

    return {
        "success": True,
        "data": {
            "scenario": scenario_id,
            "phrases": scenario["key_phrases"],
        },
    }


@router.get("/{scenario_id}/vocabulary")
async def get_vocabulary(scenario_id: str) -> Dict[str, Any]:
    """
    시나리오별 어휘 목록 반환
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found",
        )

    scenario = SCENARIOS[scenario_id]

    return {
        "success": True,
        "data": {
            "scenario": scenario_id,
            "vocabulary": scenario["vocabulary"],
        },
    }


@router.get("/{scenario_id}/start")
async def start_scenario_conversation(scenario_id: str) -> Dict[str, Any]:
    """
    시나리오 대화 시작 - 초기 메시지 반환
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found",
        )

    scenario = SCENARIOS[scenario_id]

    import random
    starter = random.choice(scenario["conversation_starters"])

    return {
        "success": True,
        "data": {
            "scenario": scenario_id,
            "initial_message": starter,
            "scenario_name": scenario["name_kr"],
            "tips": "자연스럽게 대화를 시작해보세요. 배운 표현을 사용해보세요!",
        },
    }


@router.post("/{scenario_id}/practice")
async def practice_scenario(
    scenario_id: str,
    phrase_index: int,
) -> Dict[str, Any]:
    """
    특정 표현 연습하기

    - **scenario_id**: 시나리오 ID
    - **phrase_index**: 연습할 표현의 인덱스
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found",
        )

    scenario = SCENARIOS[scenario_id]
    phrases = scenario["key_phrases"]

    if phrase_index < 0 or phrase_index >= len(phrases):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid phrase index. Must be 0-{len(phrases)-1}",
        )

    phrase = phrases[phrase_index]

    return {
        "success": True,
        "data": {
            "scenario": scenario_id,
            "phrase": phrase,
            "instructions": "이 표현을 듣고 따라해보세요.",
            "tips": [
                "천천히 발음하세요",
                "원어민 발음을 주의깊게 들으세요",
                "여러 번 반복 연습하세요",
            ],
        },
    }
