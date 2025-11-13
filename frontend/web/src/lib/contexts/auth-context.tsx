'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { authApi, holderApi } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface User {
  id: string;
  username: string;
  email?: string;
  role?: string;
  wallet_did?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  refreshAuth: () => Promise<void>;
  isAuthenticated: boolean;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const { toast } = useToast();

  // Initialize auth from localStorage
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedToken = localStorage.getItem('auth_token');
        const storedUser = localStorage.getItem('auth_user');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          
          // Verify token is still valid
          try {
            await holderApi.getWallet(storedToken);
          } catch (error) {
            // Token expired or invalid, clear auth
            localStorage.removeItem('auth_token');
            localStorage.removeItem('auth_user');
            setToken(null);
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true);
      const response = await authApi.login(credentials);
      
      const { access_token, user: userData } = response;
      
      // Store auth data
      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(userData));
      
      setToken(access_token);
      setUser(userData);

      toast({
        title: 'Login Successful',
        description: `Welcome back, ${userData.username}!`,
      });

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (error: any) {
      const errorMessage = error?.message || 'Login failed. Please check your credentials.';
      toast({
        title: 'Login Failed',
        description: errorMessage,
        variant: 'destructive',
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    try {
      setLoading(true);
      const response = await authApi.register(data);
      
      const { access_token, user: userData } = response;
      
      // Store auth data
      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(userData));
      
      setToken(access_token);
      setUser(userData);

      toast({
        title: 'Registration Successful',
        description: `Welcome to CryptLocker, ${userData.username}!`,
      });

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (error: any) {
      const errorMessage = error?.message || 'Registration failed. Please try again.';
      toast({
        title: 'Registration Failed',
        description: errorMessage,
        variant: 'destructive',
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Clear auth data
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    
    setToken(null);
    setUser(null);

    toast({
      title: 'Logged Out',
      description: 'You have been successfully logged out.',
    });

    // Redirect to login
    router.push('/login');
  };

  const refreshAuth = async () => {
    try {
      if (!token) return;
      
      // Verify token and refresh user data
      const wallet = await holderApi.getWallet(token);
      
      if (user && wallet.owner_did) {
        const updatedUser = { ...user, wallet_did: wallet.owner_did };
        setUser(updatedUser);
        localStorage.setItem('auth_user', JSON.stringify(updatedUser));
      }
    } catch (error) {
      console.error('Auth refresh error:', error);
      // Don't logout on refresh error, token might still be valid
    }
  };

  const value: AuthContextType = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    refreshAuth,
    isAuthenticated: !!token && !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
