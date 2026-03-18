import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    console.error('[API Response Error]', error.message);
    
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      console.error(`Status: ${status}`, data);
      
      switch (status) {
        case 400:
          throw new Error(data.message || '请求参数错误');
        case 404:
          throw new Error(data.message || '资源不存在');
        case 500:
          throw new Error(data.message || '服务器内部错误');
        default:
          throw new Error(data.message || `HTTP Error: ${status}`);
      }
    } else if (error.request) {
      // Request made but no response
      throw new Error('无法连接到服务器，请检查后端是否正常运行');
    } else {
      throw new Error(error.message || '网络错误');
    }
  }
);

export default apiClient;
