import { useState } from 'react'
import api from '../api/axios.api'

export function useAuth() {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    try {
      const response = await api.post('/accounts/login', { email, password });
      console.error('Login success', response);
    } catch (error) {
      console.error('Login failed', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setUser(null);
  };

  return { user, login, logout };
}