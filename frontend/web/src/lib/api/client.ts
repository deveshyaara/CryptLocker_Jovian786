import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';

// API Base URLs from environment
export const API_BASE_URLS = {
  holder: process.env.NEXT_PUBLIC_HOLDER_API_URL || 'http://localhost:8002',
  issuer: process.env.NEXT_PUBLIC_ISSUER_API_URL || 'http://localhost:8000',
  verifier: process.env.NEXT_PUBLIC_VERIFIER_API_URL || 'http://localhost:8001',
};

// Create axios instances for each service
export const createApiClient = (baseURL: string): AxiosInstance => {
  const client = axios.create({
    baseURL,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor
  client.interceptors.request.use(
    (config) => {
      // Add auth token if available
      const token = localStorage.getItem('auth_token');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      // Handle common errors
      if (error.response?.status === 401) {
        // Unauthorized - clear auth and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/login';
        }
      }
      
      return Promise.reject(error);
    }
  );

  return client;
};

// API clients for each service
export const holderClient = createApiClient(API_BASE_URLS.holder);
export const issuerClient = createApiClient(API_BASE_URLS.issuer);
export const verifierClient = createApiClient(API_BASE_URLS.verifier);

// Helper function to handle API errors
export const handleApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    // Network error
    if (!error.response) {
      return 'Network error. Please check your connection.';
    }
    // Server error with detail
    if (error.response?.data?.detail) {
      return typeof error.response.data.detail === 'string' 
        ? error.response.data.detail 
        : JSON.stringify(error.response.data.detail);
    }
    // Other server errors
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};
