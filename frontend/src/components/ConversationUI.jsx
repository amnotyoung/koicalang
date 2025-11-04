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
      setMessages([{
        role: 'assistant',
        content: initialMessage,
        timestamp: new Date().toISOString(),
      }]);

      // Synthesize initial message
      synthesizeMessage(initialMessage);
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
        const { user_input, ai_response } = response.data;

        // Add user message
        setMessages(prev => [...prev, {
          role: 'user',
          content: user_input.transcript,
          confidence: user_input.confidence,
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

        // Play AI audio response
        if (ai_response.audio) {
          const audioData = Uint8Array.from(atob(ai_response.audio), c => c.charCodeAt(0));
          const audioBlob = new Blob([audioData], { type: 'audio/mpeg' });
          const audioUrl = URL.createObjectURL(audioBlob);
          setCurrentAudio(audioUrl);

          if (audioRef.current) {
            audioRef.current.src = audioUrl;
            audioRef.current.play();
          }
        }
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

                {/* Translation for AI messages */}
                {message.role === 'assistant' && message.translation && (
                  <p className="text-sm mt-2 opacity-75">
                    💬 {message.translation}
                  </p>
                )}

                {/* Confidence for user messages */}
                {message.role === 'user' && message.confidence && (
                  <p className="text-xs mt-2 opacity-75">
                    정확도: {(message.confidence * 100).toFixed(0)}%
                  </p>
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
