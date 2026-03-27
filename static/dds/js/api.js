// static/dds/js/api.js
// API Client для взаимодействия с DRF

const API_BASE_URL = '/api/';

// CSRF Token (глобальный через window)
window.getCookie = function(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.csrftoken = window.getCookie('csrftoken');

// AJAX helper
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || JSON.stringify(error));
    }
    
    return response.json();
}

// CRUD операции для CashFlow
const CashFlowAPI = {
    // Получить список с фильтрами
    getList: async (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.date_from) params.append('date_from', filters.date_from);
        if (filters.date_to) params.append('date_to', filters.date_to);
        if (filters.status_id) params.append('status_id', filters.status_id);
        if (filters.transaction_type_id) params.append('transaction_type_id', filters.transaction_type_id);
        if (filters.category_id) params.append('category_id', filters.category_id);
        if (filters.subcategory_id) params.append('subcategory_id', filters.subcategory_id);
        
        return apiRequest(`${API_BASE_URL}cashflow/?${params}`);
    },
    
    // Создать запись
    create: async (data) => {
        return apiRequest(`${API_BASE_URL}cashflow/`, 'POST', data);
    },
    
    // Обновить запись
    update: async (id, data) => {
        return apiRequest(`${API_BASE_URL}cashflow/${id}/`, 'PUT', data);
    },
    
    // Удалить запись
    delete: async (id) => {
        return apiRequest(`${API_BASE_URL}cashflow/${id}/`, 'DELETE');
    },
    
    // Получить одну запись
    get: async (id) => {
        return apiRequest(`${API_BASE_URL}cashflow/${id}/`);
    }
};

// CRUD для справочников
const DirectoryAPI = {
    statuses: {
        getAll: () => apiRequest(`${API_BASE_URL}statuses/`),
        create: (data) => apiRequest(`${API_BASE_URL}statuses/`, 'POST', data),
        update: (id, data) => apiRequest(`${API_BASE_URL}statuses/${id}/`, 'PUT', data),
        delete: (id) => apiRequest(`${API_BASE_URL}statuses/${id}/`, 'DELETE')
    },
    
    transactionTypes: {
        getAll: () => apiRequest(`${API_BASE_URL}transaction-types/`),
        create: (data) => apiRequest(`${API_BASE_URL}transaction-types/`, 'POST', data),
        update: (id, data) => apiRequest(`${API_BASE_URL}transaction-types/${id}/`, 'PUT', data),
        delete: (id) => apiRequest(`${API_BASE_URL}transaction-types/${id}/`, 'DELETE')
    },
    
    categories: {
        getAll: () => apiRequest(`${API_BASE_URL}categories/`),
        getByTransactionType: (typeId) => apiRequest(`${API_BASE_URL}categories/by_transaction_type/?transaction_type_id=${typeId}`),
        create: (data) => apiRequest(`${API_BASE_URL}categories/`, 'POST', data),
        update: (id, data) => apiRequest(`${API_BASE_URL}categories/${id}/`, 'PUT', data),
        delete: (id) => apiRequest(`${API_BASE_URL}categories/${id}/`, 'DELETE')
    },
    
    subcategories: {
        getAll: () => apiRequest(`${API_BASE_URL}subcategories/`),
        getByCategory: (categoryId) => apiRequest(`${API_BASE_URL}subcategories/by_category/?category_id=${categoryId}`),
        create: (data) => apiRequest(`${API_BASE_URL}subcategories/`, 'POST', data),
        update: (id, data) => apiRequest(`${API_BASE_URL}subcategories/${id}/`, 'PUT', data),
        delete: (id) => apiRequest(`${API_BASE_URL}subcategories/${id}/`, 'DELETE')
    }
};

// Уведомления и форматирование доступны из window (определены в main.js)
// showAlert(), formatAmount(), formatDate() - в window
