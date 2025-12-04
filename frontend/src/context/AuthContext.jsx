import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        if (localStorage.getItem('access_token')) {
            return jwtDecode(localStorage.getItem('access_token'));
        }
        return null;
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check if token is valid on load
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const decoded = jwtDecode(token);
                if (decoded.exp < Date.now() / 1000) {
                    logout();
                } else {
                    setUser(decoded);
                }
            } catch (e) {
                logout();
            }
        }
        setLoading(false);
    }, []);

    const login = async (username, password) => {
        const response = await api.post('/auth/login/', {
            username,
            password,
        });
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        setUser(jwtDecode(response.data.access));
    };

    const register = async (username, email, password) => {
        await api.post('/auth/register/', {
            username,
            email,
            password,
        });
        // Auto login after register
        await login(username, password);
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const contextData = {
        user,
        login,
        register,
        logout,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
};
