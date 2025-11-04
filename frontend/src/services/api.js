import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Voice API
export const voiceAPI = {
  // 음성을 텍스트로 변환
  transcribe: async (audioBlob, languageCode = 'km-KH') => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('language_code', languageCode);

    const response = await api.post('/api/v1/voice/transcribe', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // 텍스트를 음성으로 변환
  synthesize: async (text, languageCode = 'km-KH', voiceGender = 'NEUTRAL') => {
    const response = await api.post('/api/v1/voice/synthesize', {
      text,
      language_code: languageCode,
      voice_gender: voiceGender,
    }, {
      responseType: 'blob',
    });
    return response.data;
  },

  // 발음 평가
  evaluatePronunciation: async (audioBlob, expectedText = null, languageCode = 'km-KH') => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    if (expectedText) {
      formData.append('expected_text', expectedText);
    }
    formData.append('language_code', languageCode);

    const response = await api.post('/api/v1/voice/evaluate-pronunciation', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // 사용 가능한 음성 목록
  getVoices: async (languageCode = 'km-KH') => {
    const response = await api.get(`/api/v1/voice/voices?language_code=${languageCode}`);
    return response.data;
  },
};

// Conversation API
export const conversationAPI = {
  // 텍스트 메시지 전송
  sendMessage: async (userInput, conversationHistory = [], scenario = 'general') => {
    const response = await api.post('/api/v1/conversation/send-message', {
      user_input: userInput,
      conversation_history: conversationHistory,
      scenario,
      language: 'Khmer',
    });
    return response.data;
  },

  // 음성 대화 (완전한 음성 루프)
  voiceConversation: async (audioBlob, scenario = 'general', languageCode = 'km-KH') => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('scenario', scenario);
    formData.append('language_code', languageCode);

    const response = await api.post('/api/v1/conversation/voice-conversation', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // 대화 평가
  evaluateConversation: async (conversationHistory, learningGoals = null) => {
    const response = await api.post('/api/v1/conversation/evaluate', {
      conversation_history: conversationHistory,
      learning_goals: learningGoals,
    });
    return response.data;
  },

  // 텍스트 분석
  analyzeText: async (text, expectedText = null, language = 'Khmer') => {
    const response = await api.post('/api/v1/conversation/analyze-text', null, {
      params: { text, expected_text: expectedText, language },
    });
    return response.data;
  },
};

// Scenarios API
export const scenariosAPI = {
  // 시나리오 목록
  list: async () => {
    const response = await api.get('/api/v1/scenarios/list');
    return response.data;
  },

  // 시나리오 상세 정보
  getDetails: async (scenarioId) => {
    const response = await api.get(`/api/v1/scenarios/${scenarioId}`);
    return response.data;
  },

  // 핵심 표현
  getPhrases: async (scenarioId) => {
    const response = await api.get(`/api/v1/scenarios/${scenarioId}/phrases`);
    return response.data;
  },

  // 어휘 목록
  getVocabulary: async (scenarioId) => {
    const response = await api.get(`/api/v1/scenarios/${scenarioId}/vocabulary`);
    return response.data;
  },

  // 대화 시작
  start: async (scenarioId) => {
    const response = await api.get(`/api/v1/scenarios/${scenarioId}/start`);
    return response.data;
  },

  // 표현 연습
  practice: async (scenarioId, phraseIndex) => {
    const response = await api.post(`/api/v1/scenarios/${scenarioId}/practice`, null, {
      params: { phrase_index: phraseIndex },
    });
    return response.data;
  },
};

export default api;
