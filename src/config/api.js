// API configuration shared by the customer site and the admin dashboard.
// Set VITE_API_BASE_URL (e.g. https://api.example.com/api/) at build time.
// In local development it falls back to the Django dev server.

const DEV_FALLBACK_API_BASE_URL = 'http://127.0.0.1:8000/api/';

const rawBaseUrl =
    import.meta.env.VITE_API_BASE_URL ||
    (import.meta.env.DEV ? DEV_FALLBACK_API_BASE_URL : '/api/');

if (!import.meta.env.VITE_API_BASE_URL && import.meta.env.PROD) {
    console.warn('VITE_API_BASE_URL is not set; API requests will go to /api/ on this origin.');
}

// Always ends with exactly one slash, so `${API_BASE_URL}events/` is valid.
export const API_BASE_URL = `${rawBaseUrl.replace(/\/+$/, '')}/`;

export const API_CONFIG = {
    baseURL: API_BASE_URL,

    // API endpoints
    endpoints: {
        auth: {
            login: 'auth/login/',
            profile: 'user/profile/'
        },
        orders: {
            list: 'orders/',
            detail: 'orders/{id}/',
            search: 'orders/search/',
            stats: 'orders/stats/',
            userOrders: 'users/{userId}/orders/',
            tickets: 'orders/{orderId}/tickets/'
        },
        tickets: {
            list: 'tickets/',
            detail: 'tickets/{id}/'
        }
    },

    // Request configuration
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000', 10),
    retryAttempts: parseInt(import.meta.env.VITE_RETRY_ATTEMPTS || '3', 10)
};

// Join the base URL and an endpoint without producing double slashes.
export const getApiUrl = (endpoint = '') => {
    return `${API_BASE_URL}${String(endpoint).replace(/^\/+/, '')}`;
};

// Helper function to replace path parameters
export const buildEndpoint = (template, params = {}) => {
    let endpoint = template;
    Object.keys(params).forEach(key => {
        endpoint = endpoint.replace(`{${key}}`, params[key]);
    });
    return endpoint;
};
