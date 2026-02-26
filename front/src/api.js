import axios from 'axios';

const API_URL = 'http://localhost:8000/';

const api = axios.create({
  baseURL: API_URL,
});

// خودکار توکن رو به header اضافه کنه
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;