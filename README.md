# Koica Lang - 크메르어 음성 대화 연습 서비스

봉사단원의 현장 적응을 위한 음성 중심 언어 학습 플랫폼

## 🎯 프로젝트 목표

봉사단원들이 크메르어 말하기와 듣기 능력을 실제 현장 시나리오를 통해 연습할 수 있도록 지원합니다.
- 음성 입력/출력 중심 인터페이스
- AI 기반 발음 피드백
- 실제 상황 기반 대화 시나리오 (시장, 교통, 동료와의 대화)

## 🏗 아키텍처

```
사용자 음성 입력 → STT (Google Cloud Speech)
                 ↓
            LLM 분석 (Gemini API) - 문법/발음/문맥 평가
                 ↓
            TTS (Google Cloud) → AI 음성 응답
```

## 🚀 시작하기

### 백엔드 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

## 📋 주요 기능

1. **음성 대화 연습**
   - 실시간 음성 인식 (크메르어)
   - AI와의 자연스러운 대화
   - 즉각적인 발음 피드백

2. **시나리오 기반 학습**
   - 시장에서 장보기
   - 뚝뚝(툭툭) 이용 및 길 찾기
   - 현지 동료/상사와 인사

3. **발음 평가**
   - 정확도, 속도, 억양 분석
   - 원어민 발음과 비교
   - 개선 제안

## 🛠 기술 스택

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: React, Vite, Tailwind CSS
- **AI/ML**: Google Gemini API, Google Cloud Speech-to-Text/Text-to-Speech
- **Database**: PostgreSQL
- **Deployment**: Docker, Docker Compose

## 📝 환경 변수 설정

`.env` 파일을 생성하고 다음 키를 설정하세요:

```
GOOGLE_CLOUD_API_KEY=your_api_key
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=postgresql://user:password@localhost:5432/koicalang
```

## 🌍 지원 언어

- 크메르어 (Cambodia/Khmer)
- 향후 확장 예정: 라오어, 베트남어 등

## 📄 라이센스

MIT License
