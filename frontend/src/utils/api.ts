import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export interface AuthRequest {
  access_key: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface AnalysisResponse {
  report: string;
}

export interface JurisdictionsResponse {
  jurisdictions: string[];
}

export interface PageContent {
  title: string;
  content: string;
}

export const authAPI = {
  login: async (data: AuthRequest): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },
};

export const analysisAPI = {
  getJurisdictions: async (): Promise<JurisdictionsResponse> => {
    const response = await api.get('/jurisdictions');
    return response.data;
  },

  analyzeDocument: async (jurisdiction: string, file: File): Promise<AnalysisResponse> => {
    const formData = new FormData();
    formData.append('jurisdiction', jurisdiction);
    formData.append('file', file);

    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  generatePDF: async (reportData: { report: string }): Promise<Blob> => {
    const response = await api.post('/generate-pdf', reportData, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export const pagesAPI = {
  getPage: async (pageName: string): Promise<PageContent> => {
    const response = await api.get(`/pages/${pageName}`);
    return response.data;
  },
};

export default api;
