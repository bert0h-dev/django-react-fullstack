import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.API_URL,
  withCredentials: true,
});

export default api;