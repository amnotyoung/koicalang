-- Koica Lang Database Schema
-- 크메르어 음성 대화 연습 서비스

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    native_language VARCHAR(10) DEFAULT 'ko',
    target_language VARCHAR(10) DEFAULT 'km',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation sessions
CREATE TABLE IF NOT EXISTS conversation_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    scenario VARCHAR(50) NOT NULL,
    language_code VARCHAR(10) DEFAULT 'km-KH',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INTEGER,
    message_count INTEGER DEFAULT 0,
    overall_score FLOAT
);

-- Conversation messages
CREATE TABLE IF NOT EXISTS conversation_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    transcript TEXT, -- STT result for user messages
    audio_url VARCHAR(500), -- Optional audio file path
    confidence FLOAT, -- STT confidence
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pronunciation evaluations
CREATE TABLE IF NOT EXISTS pronunciation_evaluations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    message_id INTEGER REFERENCES conversation_messages(id) ON DELETE CASCADE,
    transcript TEXT NOT NULL,
    expected_text TEXT,
    overall_score FLOAT NOT NULL,
    stt_confidence FLOAT,
    similarity_score FLOAT,
    pronunciation_grade VARCHAR(10),
    feedback JSONB, -- Detailed feedback from LLM
    word_analysis JSONB, -- Word-level analysis
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning progress
CREATE TABLE IF NOT EXISTS learning_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    scenario VARCHAR(50) NOT NULL,
    phrase_id VARCHAR(100),
    practice_count INTEGER DEFAULT 0,
    best_score FLOAT,
    average_score FLOAT,
    last_practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, scenario, phrase_id)
);

-- Vocabulary progress
CREATE TABLE IF NOT EXISTS vocabulary_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    word VARCHAR(255) NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    proficiency_level VARCHAR(20) DEFAULT 'beginner',
    times_practiced INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    last_practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, word, language_code)
);

-- Indexes for performance
CREATE INDEX idx_conversation_sessions_user ON conversation_sessions(user_id);
CREATE INDEX idx_conversation_messages_session ON conversation_messages(session_id);
CREATE INDEX idx_pronunciation_evaluations_user ON pronunciation_evaluations(user_id);
CREATE INDEX idx_learning_progress_user_scenario ON learning_progress(user_id, scenario);
CREATE INDEX idx_vocabulary_progress_user ON vocabulary_progress(user_id);

-- Insert sample user for testing
INSERT INTO users (username, email, full_name, native_language, target_language)
VALUES ('test_volunteer', 'test@koica.kr', '테스트 봉사단원', 'ko', 'km')
ON CONFLICT (username) DO NOTHING;
