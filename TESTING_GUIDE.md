# 음성 대화 학습 기능 테스트 가이드

이 문서는 마이크를 통한 음성 입력 기반 크메르어 학습 기능을 테스트하는 방법을 안내합니다.

## 🎯 구현된 기능

### 음성 입력 → AI 피드백 플로우

사용자가 마이크로 크메르어를 말하면:

1. **음성 인식 (STT)**: 사용자의 음성을 텍스트로 변환
2. **언어 평가 (LLM)**:
   - 발음 정확도 (0-100점)
   - 자연스러움 (0-100점)
   - 문법 피드백
   - 올바른 표현 제안
   - 개선 제안
3. **대화 응답 생성**: 시나리오에 맞는 자연스러운 크메르어 응답
4. **음성 출력 (TTS)**: AI 응답을 음성으로 재생

## 🚀 테스트 방법

### 1. 환경 설정

#### API 키 필요 사항:
```bash
# backend/.env 파일 생성
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=./credentials/google-credentials.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id
```

**Google Cloud 설정**:
- [Google Cloud Console](https://console.cloud.google.com)에서:
  - Cloud Speech-to-Text API 활성화
  - Cloud Text-to-Speech API 활성화
  - 서비스 계정 JSON 키 다운로드 → `backend/credentials/google-credentials.json`에 저장

**Gemini API**:
- [Google AI Studio](https://makersuite.google.com/app/apikey)에서 API 키 발급

#### 프론트엔드 설정:
```bash
# frontend/.env 파일 생성
VITE_API_URL=http://localhost:8000
```

### 2. 서버 실행

#### 방법 A: Docker Compose (추천)
```bash
# 루트 디렉토리에서
docker-compose up -d

# 로그 확인
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### 방법 B: 수동 실행

**백엔드:**
```bash
cd backend

# 가상환경 생성 (처음 한 번만)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**프론트엔드:**
```bash
cd frontend

# 의존성 설치 (처음 한 번만)
npm install

# 개발 서버 실행
npm run dev
```

### 3. 브라우저에서 테스트

1. **접속**: http://localhost:5173
2. **시나리오 선택**:
   - 🛒 시장에서 장보기
   - 🛺 뚝뚝(툭툭) 이용하기
   - 💼 직장 대화
3. **마이크 권한 허용** (브라우저에서 요청 시)
4. **"말하기" 버튼 클릭**하여 녹음 시작
5. **크메르어로 말하기** (예: "ជំរាបសួរ" - 안녕하세요)
6. **버튼 다시 클릭**하여 녹음 중지
7. **결과 확인**:
   - 사용자 음성이 텍스트로 변환됨
   - 정확도, 자연스러움 점수 표시
   - 발음/문법 피드백 제공
   - 개선 제안 표시
   - AI 응답이 음성으로 재생됨

## 📊 테스트 시나리오 예시

### 시나리오 1: 시장에서 장보기
```
사용자: "តម្លៃប៉ុន្មាន?" (얼마예요?)
AI 평가:
- 정확도: 85점
- 자연스러움: 90점
- 피드백: "발음이 정확합니다!"
AI 응답: "បីដុល្លារ" (3달러입니다)
```

### 시나리오 2: 뚝뚝 이용하기
```
사용자: "ទៅផ្សារកណ្តាល" (중앙시장으로 가주세요)
AI 평가:
- 정확도: 75점
- 문법 피드백: "좀 더 정중한 표현은 'សូមទៅផ្សារកណ្តាល'입니다"
AI 응답: "បាទ ចាស" (네, 알겠습니다)
```

### 시나리오 3: 직장 대화
```
사용자: "សូមអភ័យទោស" (죄송합니다)
AI 평가:
- 정확도: 95점
- 자연스러움: 95점
- 피드백: "완벽한 발음입니다!"
AI 응답: "អត់អីទេ" (괜찮습니다)
```

## 🧪 API 테스트 (고급)

### curl로 직접 테스트:

```bash
# 음성 파일로 테스트
curl -X POST "http://localhost:8000/api/v1/conversation/voice-conversation" \
  -F "audio=@test_audio.wav" \
  -F "scenario=market" \
  -F "language_code=km-KH"
```

### Swagger UI:
http://localhost:8000/docs 에서 인터랙티브 API 문서 확인

## 🔍 주요 체크포인트

- [ ] 마이크 권한이 제대로 요청되는가?
- [ ] 음성 녹음이 정상적으로 작동하는가?
- [ ] 녹음된 음성이 정확하게 텍스트로 변환되는가?
- [ ] 정확도/자연스러움 점수가 표시되는가?
- [ ] 발음/문법 피드백이 한국어로 표시되는가?
- [ ] 개선 제안이 구체적인가?
- [ ] AI 응답이 시나리오에 맞는가?
- [ ] AI 응답 음성이 자동으로 재생되는가?
- [ ] "다시 듣기" 버튼이 작동하는가?

## 🐛 문제 해결

### 마이크가 작동하지 않을 때:
- 브라우저 설정에서 마이크 권한 확인
- HTTPS 또는 localhost에서만 마이크 접근 가능 (보안 정책)

### API 오류 발생 시:
```bash
# 백엔드 로그 확인
docker-compose logs backend

# 또는
cd backend
uvicorn app.main:app --reload --log-level debug
```

### Google Cloud API 오류:
- API 키가 정확한지 확인
- Speech-to-Text, Text-to-Speech API가 활성화되어 있는지 확인
- 서비스 계정에 적절한 권한이 있는지 확인

### Gemini API 오류:
- API 키가 유효한지 확인
- API 사용량 제한을 초과하지 않았는지 확인

## 📈 개선된 기능 요약

### 백엔드 (`backend/app/api/conversation.py`)
- `/voice-conversation` 엔드포인트 강화
- `pronunciation_feedback` 필드 추가:
  - `accuracy_score`: 발음 정확도 (0-100)
  - `naturalness_score`: 자연스러움 (0-100)
  - `pronunciation_feedback`: 발음 피드백 (한국어)
  - `grammar_feedback`: 문법 피드백 (한국어)
  - `suggestions`: 개선 제안 목록
  - `correct_version`: 올바른 표현

### 프론트엔드 (`frontend/src/components/ConversationUI.jsx`)
- 사용자 메시지에 학습 피드백 표시
- 점수별 색상 구분 (80+ 녹색, 60+ 노란색, 60- 빨간색)
- 발음/문법/개선 제안을 시각적으로 표시

## 🎓 사용 팁

1. **천천히 또렷하게** 말하기
2. **짧은 문장**부터 시작
3. **피드백을 읽고** 다시 시도하기
4. **시나리오별**로 자주 사용하는 표현 연습
5. **점수가 낮으면** "올바른 표현"을 참고하여 다시 연습

## 📞 지원

문제가 발생하면:
1. 브라우저 콘솔 (F12)에서 에러 확인
2. 백엔드 로그 확인
3. API 키 및 권한 재확인
