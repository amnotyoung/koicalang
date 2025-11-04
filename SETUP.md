# 개발 환경 설정 가이드

## 📋 사전 요구사항

1. **Python 3.11+**
2. **Node.js 18+**
3. **Docker & Docker Compose** (선택사항)
4. **Google Cloud 계정** (STT/TTS용)
5. **Google Gemini API 키**

---

## 🔑 API 키 설정

### 1. Google Cloud 설정

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. 다음 API 활성화:
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API
4. 서비스 계정 생성:
   - IAM & Admin > Service Accounts
   - 새 서비스 계정 생성
   - 역할: Cloud Speech Administrator, Cloud TTS Administrator
5. JSON 키 다운로드:
   - 서비스 계정 > 키 > 키 추가 > JSON
   - `credentials/google-credentials.json`에 저장

### 2. Google Gemini API 키

1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. API 키 생성
3. `.env` 파일에 추가

---

## 🚀 로컬 개발 환경 설정

### 방법 1: Docker Compose 사용 (추천)

```bash
# 1. 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# .env 파일 편집하여 API 키 추가
nano backend/.env

# 2. Docker Compose로 전체 스택 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f

# 4. 접속
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 방법 2: 수동 설정

#### 백엔드 설정

```bash
cd backend

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
nano .env  # API 키 추가

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

#### 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env

# 개발 서버 실행
npm run dev
```

#### 데이터베이스 설정 (PostgreSQL)

```bash
# PostgreSQL 설치 및 실행 (macOS)
brew install postgresql@15
brew services start postgresql@15

# 데이터베이스 생성
createdb koicalang

# 스키마 적용
psql koicalang < database/schema.sql
```

---

## 🧪 테스트

### 백엔드 테스트

```bash
cd backend
pytest
pytest --cov=app tests/
```

### 프론트엔드 테스트

```bash
cd frontend
npm test
```

---

## 📝 환경 변수 설정

### backend/.env

```bash
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=./credentials/google-credentials.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/koicalang

# Application
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### frontend/.env

```bash
VITE_API_URL=http://localhost:8000
```

---

## 🌐 API 문서

서버 실행 후 다음 주소에서 API 문서 확인:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐛 문제 해결

### 마이크 권한 오류

- 브라우저에서 마이크 권한 허용 확인
- HTTPS 환경에서만 마이크 접근 가능 (로컬 개발은 예외)

### Google Cloud API 오류

```bash
# 인증 확인
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# 프로젝트 ID 확인
gcloud config get-value project
```

### CORS 오류

- `backend/.env`의 `ALLOWED_ORIGINS` 확인
- 프론트엔드 URL이 포함되어 있는지 확인

### 데이터베이스 연결 오류

```bash
# PostgreSQL 실행 확인
pg_isready

# 연결 테스트
psql -h localhost -U postgres -d koicalang
```

---

## 📚 추가 리소스

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [React 문서](https://react.dev/)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs)
- [Google Gemini API](https://ai.google.dev/docs)
