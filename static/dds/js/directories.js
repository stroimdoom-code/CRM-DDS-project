// static/dds/js/directories.js
// CRUD для справочников через API

const API_BASE = '/api/';

// CSRF Token (глобальный из window)
const csrftoken = window.csrftoken;

// AJAX helper
window.apiRequest = async function(url, method = 'GET', data = null) {
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
        const error = await response.json().catch(() => ({ detail: 'Ошибка сервера' }));
        throw new Error(error.detail || JSON.stringify(error));
    }
    
    if (response.status === 204) return null;
    return response.json();
}

// ==================== STATUS ====================

window.loadStatuses = async function() {
    try {
        const data = await apiRequest(`${API_BASE}statuses/`);
        const container = document.getElementById('status-list');
        container.innerHTML = data.map(s => `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <span class="badge bg-secondary px-3 py-2">${s.name}</span>
                <div>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editStatus(${s.id}, '${s.name}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteStatus(${s.id}, '${s.name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('') || '<span class="text-muted">Нет статусов</span>';
    } catch (error) {
        console.error('Ошибка загрузки статусов:', error);
        showAlert('Ошибка загрузки статусов', 'danger');
    }
}

async function saveStatus() {
    const id = document.getElementById('status-id').value;
    const name = document.getElementById('status-name').value.trim();
    
    if (!name) {
        showAlert('Введите название статуса', 'warning');
        return;
    }
    
    try {
        if (id) {
            await apiRequest(`${API_BASE}statuses/${id}/`, 'PUT', { name });
            showAlert('Статус обновлён', 'success');
        } else {
            await apiRequest(`${API_BASE}statuses/`, 'POST', { name });
            showAlert('Статус создан', 'success');
        }
        closeModal('statusModal');
        loadStatuses();
    } catch (error) {
        showAlert('Ошибка: ' + error.message, 'danger');
    }
}

async function deleteStatus(id, name) {
    if (!confirm(`Удалить статус "${name}"?`)) return;
    
    try {
        await apiRequest(`${API_BASE}statuses/${id}/`, 'DELETE');
        showAlert('Статус удалён', 'success');
        loadStatuses();
    } catch (error) {
        showAlert('Ошибка удаления: ' + error.message, 'danger');
    }
}

function editStatus(id, name) {
    document.getElementById('status-id').value = id;
    document.getElementById('status-name').value = name;
    document.getElementById('statusModalLabel').textContent = 'Редактирование статуса';
    new bootstrap.Modal(document.getElementById('statusModal')).show();
}

function openCreateStatus() {
    document.getElementById('status-id').value = '';
    document.getElementById('status-name').value = '';
    document.getElementById('statusModalLabel').textContent = 'Новый статус';
    new bootstrap.Modal(document.getElementById('statusModal')).show();
}

// ==================== TRANSACTION TYPE ====================

window.loadTransactionTypes = async function() {
    try {
        const data = await apiRequest(`${API_BASE}transaction-types/`);
        const container = document.getElementById('transactiontype-list');
        container.innerHTML = data.map(t => {
            // Используем type_color из API
            let badgeClass;
            if (t.type_color === 'income') {
                badgeClass = 'badge-income';
            } else if (t.type_color === 'expense') {
                badgeClass = 'badge-expense';
            } else {
                badgeClass = 'bg-secondary';
            }
            
            return `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <span class="badge ${badgeClass}">${t.name}</span>
                <div>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editTransactionType(${t.id}, '${t.name}', '${t.type_color}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteTransactionType(${t.id}, '${t.name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `}).join('') || '<span class="text-muted">Нет типов операций</span>';
    } catch (error) {
        console.error('Ошибка загрузки типов:', error);
        showAlert('Ошибка загрузки типов операций', 'danger');
    }
}

window.saveTransactionType = async function() {
    const id = document.getElementById('transactiontype-id').value;
    const name = document.getElementById('transactiontype-name').value.trim();
    const type_color = document.querySelector('input[name="transactiontype-color"]:checked').value;
    
    if (!name) {
        showAlert('Введите название типа', 'warning');
        return;
    }
    
    try {
        const data = { name, type_color };
        if (id) {
            await apiRequest(`${API_BASE}transaction-types/${id}/`, 'PUT', data);
            showAlert('Тип обновлён', 'success');
        } else {
            await apiRequest(`${API_BASE}transaction-types/`, 'POST', data);
            showAlert('Тип создан', 'success');
        }
        closeModal('transactiontypeModal');
        loadTransactionTypes();
    } catch (error) {
        showAlert('Ошибка: ' + error.message, 'danger');
    }
}

window.deleteTransactionType = async function(id, name) {
    if (!confirm(`Удалить тип операции "${name}"?`)) return;

    try {
        await apiRequest(`${API_BASE}transaction-types/${id}/`, 'DELETE');
        showAlert('Тип операции удалён', 'success');
        loadTransactionTypes();
        loadCategories(); // Обновляем категории (каскадное удаление)
        loadSubcategories(); // Обновляем подкатегории
    } catch (error) {
        showAlert('Ошибка удаления: ' + error.message, 'danger');
    }
}

window.editTransactionType = function(id, name, typeColor = 'other') {
    document.getElementById('transactiontype-id').value = id;
    document.getElementById('transactiontype-name').value = name;
    
    // Устанавливаем radio кнопку по type_color
    if (typeColor === 'income') {
        document.getElementById('color-income').checked = true;
    } else if (typeColor === 'expense') {
        document.getElementById('color-expense').checked = true;
    } else {
        document.getElementById('color-other').checked = true;
    }
    
    document.getElementById('transactiontypeModalLabel').textContent = 'Редактирование типа';
    new bootstrap.Modal(document.getElementById('transactiontypeModal')).show();
}

window.openCreateTransactionType = function() {
    document.getElementById('transactiontype-id').value = '';
    document.getElementById('transactiontype-name').value = '';
    document.getElementById('color-expense').checked = true; // По умолчанию списание
    document.getElementById('transactiontypeModalLabel').textContent = 'Новый тип операции';
    new bootstrap.Modal(document.getElementById('transactiontypeModal')).show();
}

// ==================== CATEGORY ====================

async function loadCategories() {
    try {
        const data = await apiRequest(`${API_BASE}categories/`);
        const container = document.getElementById('category-list');
        container.innerHTML = data.map(c => `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <div>
                    ${c.transaction_type_name === 'Пополнение' 
                        ? `<span class="badge-income me-2">${c.transaction_type_name}</span>`
                        : `<span class="badge-expense me-2">${c.transaction_type_name}</span>`
                    }
                    <span class="fw-medium">${c.name}</span>
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editCategory(${c.id}, '${c.name}', ${c.transaction_type})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory(${c.id}, '${c.name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('') || '<span class="text-muted">Нет категорий</span>';
    } catch (error) {
        console.error('Ошибка загрузки категорий:', error);
        showAlert('Ошибка загрузки категорий', 'danger');
    }
}

async function loadTransactionTypeOptions(selectId, selectedId = null) {
    try {
        const data = await apiRequest(`${API_BASE}transaction-types/`);
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Выберите тип</option>' + 
            data.map(t => `<option value="${t.id}" ${t.id == selectedId ? 'selected' : ''}>${t.name}</option>`).join('');
    } catch (error) {
        console.error('Ошибка загрузки типов:', error);
    }
}

async function saveCategory() {
    const id = document.getElementById('category-id').value;
    const name = document.getElementById('category-name').value.trim();
    const transaction_type = parseInt(document.getElementById('category-transaction-type').value);
    
    if (!name) {
        showAlert('Введите название категории', 'warning');
        return;
    }
    if (!transaction_type) {
        showAlert('Выберите тип операции', 'warning');
        return;
    }
    
    try {
        const data = { name, transaction_type };
        if (id) {
            await apiRequest(`${API_BASE}categories/${id}/`, 'PUT', data);
            showAlert('Категория обновлена', 'success');
        } else {
            await apiRequest(`${API_BASE}categories/`, 'POST', data);
            showAlert('Категория создана', 'success');
        }
        closeModal('categoryModal');
        loadCategories();
    } catch (error) {
        showAlert('Ошибка: ' + error.message, 'danger');
    }
}

window.deleteCategory = async function(id, name) {
    if (!confirm(`Удалить категорию "${name}"?`)) return;

    try {
        await apiRequest(`${API_BASE}categories/${id}/`, 'DELETE');
        showAlert('Категория удалена', 'success');
        loadCategories();
        loadSubcategories(); // Обновляем подкатегории так как они могли быть удалены каскадом
    } catch (error) {
        showAlert('Ошибка удаления: ' + error.message, 'danger');
    }
}

function editCategory(id, name, transactionType) {
    document.getElementById('category-id').value = id;
    document.getElementById('category-name').value = name;
    loadTransactionTypeOptions('category-transaction-type', transactionType);
    document.getElementById('categoryModalLabel').textContent = 'Редактирование категории';
    new bootstrap.Modal(document.getElementById('categoryModal')).show();
}

function openCreateCategory() {
    document.getElementById('category-id').value = '';
    document.getElementById('category-name').value = '';
    loadTransactionTypeOptions('category-transaction-type');
    document.getElementById('categoryModalLabel').textContent = 'Новая категория';
    new bootstrap.Modal(document.getElementById('categoryModal')).show();
}

// ==================== SUBCATEGORY ====================

async function loadSubcategories() {
    try {
        const data = await apiRequest(`${API_BASE}subcategories/`);
        const container = document.getElementById('subcategory-list');
        container.innerHTML = data.map(s => `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <div>
                    <span class="badge bg-light text-dark me-2">${s.category_name}</span>
                    <span class="fw-medium">${s.name}</span>
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editSubcategory(${s.id}, '${s.name}', ${s.category})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteSubcategory(${s.id}, '${s.name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('') || '<span class="text-muted">Нет подкатегорий</span>';
    } catch (error) {
        console.error('Ошибка загрузки подкатегорий:', error);
        showAlert('Ошибка загрузки подкатегорий', 'danger');
    }
}

async function loadCategoryOptions(selectId, selectedId = null) {
    try {
        const data = await apiRequest(`${API_BASE}categories/`);
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Выберите категорию</option>' + 
            data.map(c => `<option value="${c.id}" ${c.id == selectedId ? 'selected' : ''}>${c.name}</option>`).join('');
    } catch (error) {
        console.error('Ошибка загрузки категорий:', error);
    }
}

async function saveSubcategory() {
    const id = document.getElementById('subcategory-id').value;
    const name = document.getElementById('subcategory-name').value.trim();
    const category = parseInt(document.getElementById('subcategory-category').value);
    
    if (!name) {
        showAlert('Введите название подкатегории', 'warning');
        return;
    }
    if (!category) {
        showAlert('Выберите категорию', 'warning');
        return;
    }
    
    try {
        const data = { name, category };
        if (id) {
            await apiRequest(`${API_BASE}subcategories/${id}/`, 'PUT', data);
            showAlert('Подкатегория обновлена', 'success');
        } else {
            await apiRequest(`${API_BASE}subcategories/`, 'POST', data);
            showAlert('Подкатегория создана', 'success');
        }
        closeModal('subcategoryModal');
        loadSubcategories();
    } catch (error) {
        showAlert('Ошибка: ' + error.message, 'danger');
    }
}

window.deleteSubcategory = async function(id, name) {
    if (!confirm(`Удалить подкатегорию "${name}"?`)) return;

    try {
        await apiRequest(`${API_BASE}subcategories/${id}/`, 'DELETE');
        showAlert('Подкатегория удалена', 'success');
        loadSubcategories();
    } catch (error) {
        showAlert('Ошибка удаления: ' + error.message, 'danger');
    }
}

function editSubcategory(id, name, category) {
    document.getElementById('subcategory-id').value = id;
    document.getElementById('subcategory-name').value = name;
    loadCategoryOptions('subcategory-category', category);
    document.getElementById('subcategoryModalLabel').textContent = 'Редактирование подкатегории';
    new bootstrap.Modal(document.getElementById('subcategoryModal')).show();
}

function openCreateSubcategory() {
    document.getElementById('subcategory-id').value = '';
    document.getElementById('subcategory-name').value = '';
    loadCategoryOptions('subcategory-category');
    document.getElementById('subcategoryModalLabel').textContent = 'Новая подкатегория';
    new bootstrap.Modal(document.getElementById('subcategoryModal')).show();
}

// ==================== UTILS ====================

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) modal.hide();
}

// Инициализация при загрузке страницы
window.initDirectories = function() {
    window.loadStatuses();
    window.loadTransactionTypes();
    window.loadCategories();
    window.loadSubcategories();
};

// Запускаем когда DOM готов
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.initDirectories);
} else {
    window.initDirectories();
}
