import React, { useState, useRef, useEffect } from 'react';

/**
 * VoiceRecorder Component
 * 음성 녹음 및 재생 기능을 제공하는 큰 버튼 인터페이스
 */
const VoiceRecorder = ({ onRecordingComplete, disabled = false }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (mediaRecorderRef.current && isRecording) {
        mediaRecorderRef.current.stop();
      }
    };
  }, [isRecording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        // Use the actual MIME type from MediaRecorder
        const mimeType = mediaRecorder.mimeType || 'audio/webm;codecs=opus';
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        setAudioBlob(audioBlob);

        if (onRecordingComplete) {
          onRecordingComplete(audioBlob);
        }

        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('마이크 접근 권한이 필요합니다.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);

      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Main Recording Button */}
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled}
        className={`
          w-40 h-40 rounded-full flex items-center justify-center
          text-white font-bold text-xl transition-all
          ${isRecording
            ? 'bg-red-500 hover:bg-red-600 recording'
            : 'bg-primary-600 hover:bg-primary-700'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'shadow-2xl hover:shadow-3xl'}
        `}
      >
        {isRecording ? (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 mb-2" fill="currentColor" viewBox="0 0 20 20">
              <rect x="6" y="6" width="8" height="8" rx="1" />
            </svg>
            <span className="text-sm">중지</span>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 mb-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">말하기</span>
          </div>
        )}
      </button>

      {/* Recording Timer */}
      {isRecording && (
        <div className="text-2xl font-mono font-bold text-red-500">
          {formatTime(recordingTime)}
        </div>
      )}

      {/* Instructions */}
      <p className="text-gray-600 text-center max-w-md">
        {isRecording
          ? '녹음 중입니다. 크메르어로 말해보세요.'
          : '버튼을 눌러 녹음을 시작하세요.'
        }
      </p>

      {/* Audio Playback (if recorded) */}
      {audioBlob && !isRecording && (
        <div className="mt-4">
          <audio controls src={URL.createObjectURL(audioBlob)} className="rounded-lg" />
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
