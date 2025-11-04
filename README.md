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

## 🚀 빠른 시작

### 필수 준비사항
1. Google Cloud API 키 (STT/TTS)
2. Google Gemini API 키
3. Python 3.11+, Node.js 18+

**자세한 설정 방법은 [SETUP.md](./SETUP.md) 참고**
**테스트 가이드는 [TESTING_GUIDE.md](./TESTING_GUIDE.md) 참고**

### Docker Compose로 실행 (추천)

```bash
# 1. 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# .env 파일을 편집하여 API 키 추가

# 2. 실행
docker-compose up -d

# 3. 접속
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 수동 실행

**백엔드:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**프론트엔드:**
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
   - **NEW!** 정확도 및 자연스러움 점수 (0-100점)

2. **시나리오 기반 학습**
   - 시장에서 장보기
   - 뚝뚝(툭툭) 이용 및 길 찾기
   - 현지 동료/상사와 인사

3. **AI 기반 학습 피드백**
   - **발음 평가**: 정확도 점수와 구체적인 피드백
   - **문법 분석**: 문법 오류 지적 및 올바른 표현 제시
   - **자연스러움 평가**: 원어민스러운 표현인지 평가
   - **개선 제안**: 구체적이고 실용적인 학습 팁 제공
   - 모든 피드백이 **한국어**로 제공

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
