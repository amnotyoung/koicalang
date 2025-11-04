import React, { useState } from 'react';
import ScenarioSelector from './components/ScenarioSelector';
import ConversationUI from './components/ConversationUI';

function App() {
  const [currentView, setCurrentView] = useState('scenario-selection');
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [initialMessage, setInitialMessage] = useState(null);

  const handleSelectScenario = (scenarioId, startMessage) => {
    setSelectedScenario(scenarioId);
    setInitialMessage(startMessage);
    setCurrentView('conversation');
  };

  const handleBackToScenarios = () => {
    setCurrentView('scenario-selection');
    setSelectedScenario(null);
    setInitialMessage(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {currentView === 'scenario-selection' ? (
        <ScenarioSelector onSelectScenario={handleSelectScenario} />
      ) : (
        <div className="h-screen flex flex-col">
          {/* Header */}
          <header className="bg-white shadow-md p-4">
            <div className="max-w-4xl mx-auto flex items-center justify-between">
              <button
                onClick={handleBackToScenarios}
                className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium text-gray-700 transition-colors"
              >
                ← 시나리오 선택
              </button>
              <h1 className="text-xl font-bold text-gray-800">
                {selectedScenario === 'market' && '🛒 시장에서 장보기'}
                {selectedScenario === 'transport' && '🛺 뚝뚝 이용하기'}
                {selectedScenario === 'workplace' && '💼 직장 대화'}
              </h1>
              <div className="w-32" /> {/* Spacer for centering */}
            </div>
          </header>

          {/* Conversation Area */}
          <main className="flex-1 overflow-hidden p-4">
            <ConversationUI
              scenario={selectedScenario}
              initialMessage={initialMessage}
            />
          </main>
        </div>
      )}
    </div>
  );
}

export default App;
