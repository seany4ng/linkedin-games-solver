import axios from 'axios';

const client = axios.create({
    baseURL: 'https://kaiser--linkedin-games-solver-run-app.modal.run',
    // baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Optional: Add interceptors
client.interceptors.request.use((config: { headers: { Authorization: string; }; }) => {
    // Attach auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

client.interceptors.response.use(
    (response: any) => response,
    (error: any) => {
        // Handle errors globally if needed
        console.error('API Error:', error);
        return Promise.reject(error);
    }
);

export default client;