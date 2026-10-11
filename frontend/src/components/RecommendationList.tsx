import React from 'react';
import type { Recommendation } from '../types';
import { getScoreStyle } from '../utils';

interface RecommendationListProps {
  isPanelOpen: boolean;
  recommendations: Recommendation[];
  onExpandCard: (index: number) => void;
}

export const RecommendationList: React.FC<RecommendationListProps> = ({
  isPanelOpen,
  recommendations,
  onExpandCard
}) => {
  return (
    <div className={`results-panel ${isPanelOpen ? 'show' : ''}`}>
      <div className="recommendations-container">
        <h2 style={{ marginBottom: '1.5rem', marginTop: 0 }}>Your Recommended Learning Paths</h2>
        {recommendations.length > 0 ? (
          recommendations.map((rec, idx) => (
            <div
              key={idx}
              className="rec-card"
              onClick={() => onExpandCard(idx)}
              style={{ cursor: 'pointer', transition: 'all 0.3s ease' }}
            >
              <div className="course-header" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1rem' }}>
                <div className="course-id" style={{ display: 'flex', alignItems: 'flex-start', margin: 0 }}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, color: '#3b82f6', marginTop: '2px', marginRight: '0.5rem' }}>
                    <path d="M9 18l6-6-6-6" />
                  </svg>
                  <span style={{ lineHeight: 1.3 }}>{rec.path_name}</span>
                </div>
                <div className="score-badge" style={{ alignSelf: 'flex-start', ...getScoreStyle(rec.score), padding: '4px 10px', borderRadius: '12px', fontSize: '0.85rem', fontWeight: 'bold', whiteSpace: 'nowrap' }}>
                  Recommendation: {rec.score}
                </div>
              </div>

              <div className="course-rationale">{rec.rationale}</div>
              <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#2563eb', fontWeight: 600 }}>
                Click to view full curriculum ↗
              </div>
            </div>
          ))
        ) : (
          <div className="mastered-card">
            <div className="mastered-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ margin: '0 auto' }}>
                <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
                <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
                <path d="M4 22h16" />
                <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
                <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
                <path d="M18 2H6v7c0 3.31 2.69 6 6 6s6-2.69 6-6V2Z" />
              </svg>
            </div>
            <div className="mastered-title">No Recommendations Found</div>
            <div className="mastered-text">Try adjusting your goal or expected level.</div>
          </div>
        )}
      </div>
    </div>
  );
};
