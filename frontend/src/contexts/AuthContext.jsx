import React, { createContext, useContext, useState, useEffect } from 'react';
import client from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('gym_token');
    const savedUser = localStorage.getItem('gym_user');
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('gym_token');
        localStorage.removeItem('gym_user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const res = await client.post('/auth/login', { email, password });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('gym_token', access_token);
    localStorage.setItem('gym_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const register = async (formData) => {
    const res = await client.post('/auth/register', formData);
    const { access_token, user: userData } = res.data;
    localStorage.setItem('gym_token', access_token);
    localStorage.setItem('gym_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const logout = () => {
    localStorage.removeItem('gym_token');
    localStorage.removeItem('gym_user');
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const res = await client.get('/auth/me');
      setUser(res.data);
      localStorage.setItem('gym_user', JSON.stringify(res.data));
      return res.data;
    } catch {
      logout();
    }
  };

  const isAdmin = () => user?.role === 'admin';
  const isPremium = () => user?.membership_type === 'premium' || user?.role === 'admin';
  const isLoggedIn = () => !!user;

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser, isAdmin, isPremium, isLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
