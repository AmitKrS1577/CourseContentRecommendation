import React from 'react';
import type { Recommendation } from '../types';
import { getScoreStyle } from '../utils';

interface CourseModalProps {
  recommendation: Recommendation;
  onClose: () => void;
}

export const CourseModal: React.FC<CourseModalProps> = ({ recommendation, onClose }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>

        <h2 style={{ marginTop: 0, marginBottom: '0.5rem', color: '#0f172a', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {recommendation.path_name}
        </h2>

        <div style={{ display: 'inline-block', ...getScoreStyle(recommendation.score), padding: '4px 10px', borderRadius: '12px', fontSize: '0.9rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
          Recommendation: {recommendation.score}
        </div>

        <p style={{ fontSize: '1rem', color: '#334155', lineHeight: 1.6, marginBottom: '2rem' }}>
          {recommendation.rationale}
        </p>

        <strong style={{ fontSize: '1.1rem', color: '#0f172a', display: 'block', marginBottom: '1rem', borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem' }}>Course Curriculum:</strong>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {recommendation.courses.map((course, i) => (
            <div key={i} style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: '8px', borderLeft: '4px solid #2563eb' }}>
              <div style={{ fontWeight: 700, fontSize: '1.05rem', color: '#0f172a', marginBottom: '0.5rem' }}>
                Step {i + 1}: {course.course_title}
              </div>
              <p style={{ margin: 0, fontSize: '0.95rem', color: '#475569', lineHeight: 1.5, marginBottom: '1rem' }}>
                {course.description}
              </p>
              <a href={course.url} target="_blank" rel="noopener noreferrer" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', background: '#eff6ff', color: '#2563eb', padding: '0.4rem 0.75rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 600, textDecoration: 'none' }}>
                Start Course ↗
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
