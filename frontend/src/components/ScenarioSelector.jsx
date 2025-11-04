import React, { useState, useEffect } from 'react';
import { scenariosAPI } from '../services/api';

/**
 * ScenarioSelector Component
 * 학습 시나리오 선택 화면
 */
const ScenarioSelector = ({ onSelectScenario }) => {
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [scenarioDetails, setScenarioDetails] = useState(null);

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      const response = await scenariosAPI.list();
      if (response.success) {
        setScenarios(response.data.scenarios);
      }
    } catch (error) {
      console.error('Failed to load scenarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleScenarioClick = async (scenario) => {
    setSelectedScenario(scenario.id);

    try {
      const response = await scenariosAPI.getDetails(scenario.id);
      if (response.success) {
        setScenarioDetails(response.data);
      }
    } catch (error) {
      console.error('Failed to load scenario details:', error);
    }
  };

  const handleStartConversation = async () => {
    if (!selectedScenario) return;

    try {
      const response = await scenariosAPI.start(selectedScenario);
      if (response.success) {
        onSelectScenario(selectedScenario, response.data.initial_message);
      }
    } catch (error) {
      console.error('Failed to start conversation:', error);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyLabel = (difficulty) => {
    switch (difficulty) {
      case 'beginner':
        return '초급';
      case 'intermediate':
        return '중급';
      case 'advanced':
        return '고급';
      default:
        return difficulty;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-2">
        크메르어 대화 연습
      </h1>
      <p className="text-center text-gray-600 mb-8">
        실전 상황에서 사용하는 크메르어를 연습해보세요
      </p>

      {!scenarioDetails ? (
        /* Scenario Selection Grid */
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {scenarios.map((scenario) => (
            <button
              key={scenario.id}
              onClick={() => handleScenarioClick(scenario)}
              className={`
                p-6 rounded-2xl text-left transition-all
                ${selectedScenario === scenario.id
                  ? 'bg-primary-500 text-white shadow-2xl scale-105'
                  : 'bg-white hover:bg-gray-50 shadow-lg hover:shadow-xl'
                }
              `}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-4xl">
                  {scenario.id === 'market' && '🛒'}
                  {scenario.id === 'transport' && '🛺'}
                  {scenario.id === 'workplace' && '💼'}
                </span>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    selectedScenario === scenario.id
                      ? 'bg-white text-primary-700'
                      : getDifficultyColor(scenario.difficulty)
                  }`}
                >
                  {getDifficultyLabel(scenario.difficulty)}
                </span>
              </div>

              <h3 className="text-xl font-bold mb-2">
                {scenario.name_kr}
              </h3>
              <p className="text-sm opacity-90">
                {scenario.description}
              </p>
            </button>
          ))}
        </div>
      ) : (
        /* Scenario Details */
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <button
            onClick={() => {
              setScenarioDetails(null);
              setSelectedScenario(null);
            }}
            className="mb-6 text-primary-600 hover:text-primary-700 font-medium"
          >
            ← 뒤로 가기
          </button>

          <h2 className="text-2xl font-bold mb-4">{scenarioDetails.name_kr}</h2>
          <p className="text-gray-600 mb-6">{scenarioDetails.description}</p>

          {/* Key Phrases */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-4">핵심 표현</h3>
            <div className="space-y-3">
              {scenarioDetails.key_phrases.map((phrase, index) => (
                <div
                  key={index}
                  className="p-4 bg-blue-50 rounded-lg"
                >
                  <p className="text-lg font-semibold text-gray-800">
                    {phrase.khmer}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {phrase.romanization}
                  </p>
                  {phrase.pronunciation_kr && (
                    <p className="text-sm text-gray-500 mt-0.5 italic">
                      ({phrase.pronunciation_kr})
                    </p>
                  )}
                  <p className="text-sm text-primary-700 mt-1">
                    💬 {phrase.korean}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Vocabulary */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-4">주요 어휘</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {scenarioDetails.vocabulary.map((word, index) => (
                <div
                  key={index}
                  className="p-3 bg-gray-50 rounded-lg"
                >
                  <p className="font-semibold text-gray-800">{word.khmer}</p>
                  <p className="text-xs text-gray-500">{word.romanization}</p>
                  <p className="text-sm text-primary-600 mt-1">{word.meaning}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Start Button */}
          <button
            onClick={handleStartConversation}
            className="w-full py-4 bg-primary-600 hover:bg-primary-700 text-white font-bold text-lg rounded-xl shadow-lg transition-colors"
          >
            대화 시작하기
          </button>
        </div>
      )}
    </div>
  );
};

export default ScenarioSelector;
