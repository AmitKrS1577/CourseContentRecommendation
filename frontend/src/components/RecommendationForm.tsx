import React, { useState } from 'react';

interface RecommendationFormProps {
  loading: boolean;
  error: string;
  onFetchRecommendations: (goal: string, expectedLevel: string, completedModules: string) => void;
}

export const RecommendationForm: React.FC<RecommendationFormProps> = ({ loading, error, onFetchRecommendations }) => {
  const [goal, setGoal] = useState('');
  const [expectedLevel, setExpectedLevel] = useState('advanced');
  const [completedModules, setCompletedModules] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFetchRecommendations(goal, expectedLevel, completedModules);
  };

  return (
    <div className="form-panel">
      <h1 className="title">NextStep AI</h1>
      <p className="subtitle">Discover your personalized learning path</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Stated Goal</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g. I want to learn machine learning algorithms"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Completed Modules (Optional)</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g. Python Basics, Math 101"
            value={completedModules}
            onChange={(e) => setCompletedModules(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Expected Knowledge Level</label>
          <select
            className="form-control"
            value={expectedLevel}
            onChange={(e) => setExpectedLevel(e.target.value)}
          >
            <option value="beginner">Beginner (Foundations Only)</option>
            <option value="intermediate">Intermediate (Fundamentals + Practical)</option>
            <option value="advanced">Advanced (Complete Mastery)</option>
          </select>
        </div>

        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Analyzing Profile...' : 'Get Path Recommendations'}
        </button>

        <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid #e2e8f0' }}>
          <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '0.75rem', fontWeight: 600 }}>Or test with a simulated profile:</p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button type="button" onClick={() => { setGoal('I want to learn Python for data analysis'); setExpectedLevel('beginner'); setCompletedModules(''); }} style={{ background: '#f1f5f9', color: '#334155', border: '1px solid #cbd5e1', padding: '6px 12px', borderRadius: '20px', fontSize: '0.8rem', cursor: 'pointer', flex: 1, whiteSpace: 'nowrap', transition: 'background 0.2s' }} onMouseOver={(e) => e.currentTarget.style.background = '#e2e8f0'} onMouseOut={(e) => e.currentTarget.style.background = '#f1f5f9'}>
              1: Data Beginner
            </button>
            <button type="button" onClick={() => { setGoal('I want to build full stack web apps with React'); setExpectedLevel('intermediate'); setCompletedModules('HTML Basics, CSS Layouts'); }} style={{ background: '#f1f5f9', color: '#334155', border: '1px solid #cbd5e1', padding: '6px 12px', borderRadius: '20px', fontSize: '0.8rem', cursor: 'pointer', flex: 1, whiteSpace: 'nowrap', transition: 'background 0.2s' }} onMouseOver={(e) => e.currentTarget.style.background = '#e2e8f0'} onMouseOut={(e) => e.currentTarget.style.background = '#f1f5f9'}>
              2: Web Dev Interm
            </button>
            <button type="button" onClick={() => { setGoal('I need to master Convolutional Neural Networks'); setExpectedLevel('advanced'); setCompletedModules('Python Basics, Machine Learning 101, Neural Networks'); }} style={{ background: '#f1f5f9', color: '#334155', border: '1px solid #cbd5e1', padding: '6px 12px', borderRadius: '20px', fontSize: '0.8rem', cursor: 'pointer', flex: 1, whiteSpace: 'nowrap', transition: 'background 0.2s' }} onMouseOver={(e) => e.currentTarget.style.background = '#e2e8f0'} onMouseOut={(e) => e.currentTarget.style.background = '#f1f5f9'}>
              3: ML Advanced
            </button>
          </div>
        </div>
      </form>

      {error && <p style={{ color: '#ef4444', marginTop: '1rem', textAlign: 'center' }}>{error}</p>}

      {loading && (
        <div className="loader">
          <div className="spinner"></div>
        </div>
      )}
    </div>
  );
};
