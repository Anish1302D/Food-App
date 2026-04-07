const API_BASE = 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    if (err.message === 'Failed to fetch') {
      throw new Error('Cannot connect to server. Make sure the backend is running on port 8000.');
    }
    throw err;
  }
}

// ======================== Profile API ========================
export const profileAPI = {
  create: (data) => request('/profile/', { method: 'POST', body: JSON.stringify(data) }),
  get: (userId = 1) => request(`/profile/${userId}`),
};

// ======================== Recommendation API ========================
export const recommendAPI = {
  getMeals: (data) => request('/recommend/', { method: 'POST', body: JSON.stringify(data) }),
  getInstant: (userId = 1) => request('/recommend/instant', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  }),
};

// ======================== Food Log API ========================
export const foodLogAPI = {
  log: (data) => request('/log/', { method: 'POST', body: JSON.stringify(data) }),
  getToday: (userId = 1) => request(`/log/${userId}/today`),
  getSummary: (userId = 1) => request(`/log/${userId}/summary`),
  delete: (logId) => request(`/log/${logId}`, { method: 'DELETE' }),
};

// ======================== Feedback API ========================
export const feedbackAPI = {
  get: (userId = 1) => request(`/feedback/${userId}`),
};

// ======================== Health Score API ========================
export const healthScoreAPI = {
  get: (userId = 1) => request(`/health-score/${userId}`),
};
