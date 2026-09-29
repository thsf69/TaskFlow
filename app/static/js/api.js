// API Helper
const API = {
    async request(url, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json'
        };
        
        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        if (config.body && typeof config.body !== 'string') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            const contentType = response.headers.get("content-type");
            let data = null;
            
            if (contentType && contentType.indexOf("application/json") !== -1) {
                data = await response.json();
            }

            if (!response.ok) {
                if (response.status === 401 && window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
                throw new Error(data?.error || `HTTP error! status: ${response.status}`);
            }
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    auth: {
        login: (credentials) => API.request('/api/login', { method: 'POST', body: credentials }),
        register: (userData) => API.request('/api/register', { method: 'POST', body: userData }),
        logout: () => API.request('/api/logout', { method: 'POST' })
    },

    tasks: {
        getAll: (params = '') => API.request(`/api/tasks${params ? '?' + params : ''}`),
        getOne: (id) => API.request(`/api/tasks/${id}`),
        create: (taskData) => API.request('/api/tasks', { method: 'POST', body: taskData }),
        update: (id, taskData) => API.request(`/api/tasks/${id}`, { method: 'PUT', body: taskData }),
        delete: (id) => API.request(`/api/tasks/${id}`, { method: 'DELETE' }),
        updateStatus: (id, status) => API.request(`/api/tasks/${id}/status`, { method: 'PATCH', body: { status } })
    },
    
    dashboard: {
        getStats: () => API.request('/api/dashboard')
    }
};

// UI Helpers
function showAlert(message, type = 'danger', containerId = 'alert-container') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

function formatDate(dateString) {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}
