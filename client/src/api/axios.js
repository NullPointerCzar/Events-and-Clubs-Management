import axios from "axios";

// 1. Create a central instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/", // Your Django URL
  headers: {
    "Content-Type": "application/json",
  },
});

// 2. Interceptor: Automatically add the Token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // or from Context
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

export default api;
