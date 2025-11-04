import React, { useState, useEffect, useRef } from 'react';
import VoiceRecorder from './VoiceRecorder';
import { conversationAPI, voiceAPI } from '../services/api';

/**
 * ConversationUI Component
 * 음성 대화 인터페이스
 */
const ConversationUI = ({ scenario = 'general', initialMessage = null }) => {
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentAudio, setCurrentAudio] = useState(null);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    // Add initial AI message if provided
    if (initialMessage) {
      // Handle both string (legacy) and object (new) format
      const messageContent = typeof initialMessage === 'string'
        ? initialMessage
        : initialMessage.khmer;

      const messageData = {
        role: 'assistant',
        content: messageContent,
        timestamp: new Date().toISOString(),
      };

      // Add translation and romanization if available
      if (typeof initialMessage === 'object') {
        messageData.translation = initialMessage.korean;
        messageData.romanization = initialMessage.romanization;
        messageData.romanizationKr = initialMessage.romanization_kr;
      }

      setMessages([messageData]);

      // Synthesize initial message - disabled temporarily as Khmer TTS may not be available
      // synthesizeMessage(messageContent);
    }
  }, [initialMessage]);

  useEffect(() => {
    // Auto-scroll to bottom
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const synthesizeMessage = async (text) => {
    try {
      const audioBlob = await voiceAPI.synthesize(text, 'km-KH');
      const audioUrl = URL.createObjectURL(audioBlob);
      setCurrentAudio(audioUrl);

      // Auto-play
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play();
      }
    } catch (error) {
      console.error('TTS Error:', error);
    }
  };

  const handleRecordingComplete = async (audioBlob) => {
    setIsProcessing(true);

    try {
      // Send audio to backend for full conversation
      const response = await conversationAPI.voiceConversation(
        audioBlob,
        scenario,
        'km-KH'
      );

      if (response.success) {
        const { user_input, pronunciation_feedback, ai_response } = response.data;

        // Add user message with pronunciation feedback
        setMessages(prev => [...prev, {
          role: 'user',
          content: user_input.transcript,
          confidence: user_input.confidence,
          feedback: pronunciation_feedback,
          timestamp: new Date().toISOString(),
        }]);

        // Add AI response
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: ai_response.text,
          translation: ai_response.translation_kr,
          keyPhrases: ai_response.key_phrases,
          culturalNote: ai_response.cultural_note,
          timestamp: new Date().toISOString(),
        }]);

        // Play AI audio response - disabled as Khmer TTS not available
        // if (ai_response.audio) {
        //   const audioData = Uint8Array.from(atob(ai_response.audio), c => c.charCodeAt(0));
        //   const audioBlob = new Blob([audioData], { type: 'audio/mpeg' });
        //   const audioUrl = URL.createObjectURL(audioBlob);
        //   setCurrentAudio(audioUrl);

        //   if (audioRef.current) {
        //     audioRef.current.src = audioUrl;
        //     audioRef.current.play();
        //   }
        // }
      }
    } catch (error) {
      console.error('Conversation error:', error);
      alert('오류가 발생했습니다. 다시 시도해주세요.');
    } finally {
      setIsProcessing(false);
    }
  };

  const replayAudio = () => {
    if (audioRef.current && currentAudio) {
      audioRef.current.play();
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white rounded-t-2xl shadow-inner">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-xl">대화를 시작하세요</p>
            <p className="text-sm mt-2">아래 버튼을 눌러 말해보세요</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-4 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="text-lg">{message.content}</p>

                {/* Translation and pronunciation for AI messages */}
                {message.role === 'assistant' && (
                  <div className="mt-2 space-y-1">
                    {message.translation && (
                      <p className="text-sm opacity-75">
                        💬 {message.translation}
                      </p>
                    )}
                    {message.romanization && (
                      <p className="text-xs opacity-60 italic">
                        🔤 {message.romanization}
                      </p>
                    )}
                    {message.romanizationKr && (
                      <p className="text-xs opacity-60">
                        🗣️ {message.romanizationKr}
                      </p>
                    )}
                  </div>
                )}

                {/* Feedback for user messages */}
                {message.role === 'user' && message.feedback && (
                  <div className="mt-3 space-y-2 text-sm border-t border-white/30 pt-3">
                    {/* Scores */}
                    <div className="flex gap-4">
                      <div className="flex items-center gap-1">
                        <span className="font-semibold">정확도:</span>
                        <span className={`font-bold ${
                          message.feedback.accuracy_score >= 80 ? 'text-green-300' :
                          message.feedback.accuracy_score >= 60 ? 'text-yellow-300' :
                          'text-red-300'
                        }`}>
                          {message.feedback.accuracy_score}점
                        </span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span className="font-semibold">자연스러움:</span>
                        <span className={`font-bold ${
                          message.feedback.naturalness_score >= 80 ? 'text-green-300' :
                          message.feedback.naturalness_score >= 60 ? 'text-yellow-300' :
                          'text-red-300'
                        }`}>
                          {message.feedback.naturalness_score}점
                        </span>
                      </div>
                    </div>

                    {/* Pronunciation Feedback */}
                    {message.feedback.pronunciation_feedback && (
                      <div>
                        <p className="font-semibold text-xs mb-1">📢 발음 피드백:</p>
                        <p className="text-xs opacity-90">{message.feedback.pronunciation_feedback}</p>
                      </div>
                    )}

                    {/* Grammar Feedback */}
                    {message.feedback.grammar_feedback && (
                      <div>
                        <p className="font-semibold text-xs mb-1">📝 문법 피드백:</p>
                        <p className="text-xs opacity-90">{message.feedback.grammar_feedback}</p>
                      </div>
                    )}

                    {/* Correct Version */}
                    {message.feedback.correct_version && message.feedback.correct_version !== message.content && (
                      <div>
                        <p className="font-semibold text-xs mb-1">✨ 올바른 표현:</p>
                        <p className="text-xs opacity-90 font-medium">{message.feedback.correct_version}</p>
                      </div>
                    )}

                    {/* Suggestions */}
                    {message.feedback.suggestions && message.feedback.suggestions.length > 0 && (
                      <div>
                        <p className="font-semibold text-xs mb-1">💡 개선 제안:</p>
                        <ul className="list-disc list-inside text-xs opacity-90 space-y-1">
                          {message.feedback.suggestions.map((suggestion, i) => (
                            <li key={i}>{suggestion}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* STT Confidence */}
                    {message.confidence && (
                      <p className="text-xs mt-2 opacity-75">
                        음성 인식 신뢰도: {(message.confidence * 100).toFixed(0)}%
                      </p>
                    )}
                  </div>
                )}

                {/* Key phrases */}
                {message.keyPhrases && message.keyPhrases.length > 0 && (
                  <div className="mt-2 text-sm opacity-75">
                    <p className="font-semibold">핵심 표현:</p>
                    <ul className="list-disc list-inside">
                      {message.keyPhrases.map((phrase, i) => (
                        <li key={i}>{phrase}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Cultural note */}
                {message.culturalNote && (
                  <div className="mt-2 text-sm opacity-75 border-t pt-2">
                    <p className="font-semibold">💡 문화 팁:</p>
                    <p>{message.culturalNote}</p>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Audio Player (hidden) */}
      <audio ref={audioRef} style={{ display: 'none' }} />

      {/* Replay Button */}
      {currentAudio && (
        <div className="flex justify-center p-2 bg-white">
          <button
            onClick={replayAudio}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-sm font-medium"
          >
            🔊 다시 듣기
          </button>
        </div>
      )}

      {/* Voice Recorder */}
      <div className="p-6 bg-gradient-to-t from-blue-50 to-white rounded-b-2xl shadow-lg">
        <VoiceRecorder
          onRecordingComplete={handleRecordingComplete}
          disabled={isProcessing}
        />
        {isProcessing && (
          <div className="text-center mt-4">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p className="mt-2 text-gray-600">처리 중...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationUI;
