import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ToxicityBatchRequest {
  model: {
    name: string;
    description: string;
    base_url: string | null;
  };
  num_samples: number;
  random: boolean;
  database_prompts: boolean;
  user_prompts: string[] | null;
  user_topics: string[] | null;
}

export interface BiasRequest {
  model: {
    name: string;
    description: string;
    base_url: string | null;
  };
  prompts: {
    prompt_library_path: string;
  };
  topics: string[];
}

export const api = {
  health: {
    check: () => apiClient.get('/health'),
  },
  toxicity: {
    batch: (data: ToxicityBatchRequest) =>
      apiClient.post('/toxicity-detection-batch', data),
    realtime: (prompt: string) =>
      apiClient.post('/toxicity-detection-realtime', { prompt }),
  },
  bias: {
    batch: (data: BiasRequest) =>
      apiClient.post('/bias-detection-batch', data),
    realtime: (prompt: string) =>
      apiClient.post('/bias-detection-realtime', { prompt }),
  },
};

export default api;