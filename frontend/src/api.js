import axios from 'axios';
import jwtDecode from 'jwt-decode'; 

const api = axios.create({
    baseURL: 'https://benchmate-django.onrender.com/api',
});

export const fastApi = axios.create({
    baseURL: 'https://benchmate-fastapi.onrender.com',
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            const decoded = jwtDecode(token);
            const currentTime = Date.now() / 1000;
            if (decoded.exp < currentTime) {
                // Token expired
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            } else {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
