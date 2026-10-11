import { useState } from 'react';
import './index.css';
import type { Recommendation } from './types';
import { RecommendationForm } from './components/RecommendationForm';
import { RecommendationList } from './components/RecommendationList';
import { CourseModal } from './components/CourseModal';

function App() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [expandedCard, setExpandedCard] = useState<number | null>(null);
  const [hasCompletedSearch, setHasCompletedSearch] = useState(false);

  const fetchRecommendations = async (goal: string, expectedLevel: string, completedModules: string) => {
    setLoading(true);
    setHasCompletedSearch(false);
    setError('');
    setExpandedCard(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'user_custom',
          stated_goal: goal,
          expected_level: expectedLevel,
          completed_modules: completedModules,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
      setHasCompletedSearch(true);
    } catch (err: any) {
      setError(err.message || 'An error occurred fetching recommendations.');
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const isPanelOpen = !loading && hasCompletedSearch;

  return (
    <div className={`app-container ${isPanelOpen ? 'has-results' : ''}`}>
      <div className="content-wrapper">
        
        {/* Left Form Panel */}
        <RecommendationForm 
          loading={loading} 
          error={error}
          onFetchRecommendations={fetchRecommendations} 
        />

        {/* Right Results Panel */}
        <RecommendationList 
          isPanelOpen={isPanelOpen} 
          recommendations={recommendations} 
          onExpandCard={setExpandedCard} 
        />
        
      </div>

      {expandedCard !== null && recommendations[expandedCard] && (
        <CourseModal 
          recommendation={recommendations[expandedCard]} 
          onClose={() => setExpandedCard(null)} 
        />
      )}
    </div>
  );
}

export default App;
