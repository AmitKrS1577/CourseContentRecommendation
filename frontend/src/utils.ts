export const getScoreStyle = (score: string) => {
  const s = score.toLowerCase();
  if (s.includes('high')) {
    return { background: '#dcfce7', color: '#166534' }; // Green
  }
  if (s.includes('mid')) {
    return { background: '#ffedd5', color: '#c2410c' }; // Orange/Yellow
  }
  if (s.includes('low')) {
    return { background: '#fee2e2', color: '#b91c1c' }; // Red
  }
  return { background: '#f1f5f9', color: '#475569' }; // Default gray
};
