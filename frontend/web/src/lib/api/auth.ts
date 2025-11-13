import { holderClient, handleApiError } from './client';

// Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    email?: string;
    role?: string;
    wallet_did?: string;
  };
}

// Auth API functions
export const authApi = {
  /**
   * Login user
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      // Convert to URLSearchParams for application/x-www-form-urlencoded
      const params = new URLSearchParams();
      params.append('username', credentials.username);
      params.append('password', credentials.password);

      const response = await holderClient.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Register new user
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await holderClient.post('/auth/register', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Verify token validity
   */
  async verifyToken(token: string): Promise<boolean> {
    try {
      await holderClient.get('/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return true;
    } catch (error) {
      return false;
    }
  },

  /**
   * Get current user info
   */
  async getCurrentUser(token: string): Promise<any> {
    try {
      const response = await holderClient.get('/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
