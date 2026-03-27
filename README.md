# CRM DDS — Система учета движения денежных средств

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Веб-приложение для управления движением денежных средств (ДДС) компании или частного лица.

---

## 📋 Оглавление

- [Возможности](#-возможности)
- [Технологии](#-технологии)
- [Установка](#-установка)
- [Настройка](#-настройка)
- [Запуск](#-запуск)
- [Тесты](#-тесты)
- [Структура проекта](#-структура-проекта)
- [Безопасность](#-безопасность)
- [Деплой](#-деплой)
- [Лицензия](#-лицензия)

---

## ✨ Возможности

### Управление записями ДДС
- ✅ Создание, редактирование, удаление записей о движении денежных средств
- ✅ Просмотр списка всех записей
- ✅ Расширенная фильтрация по:
  - Дате (период с/по)
  - Статусу (Бизнес, Личное, Налог)
  - Типу операции (Пополнение, Списание)
  - Категории
  - Подкатегории

### REST API (Django REST Framework)
- ✅ Полный CRUD для всех сущностей
- ✅ Фильтрация данных через API
- ✅ Каскадные фильтры (тип → категория → подкатегория)
- ✅ Валидация данных на стороне API

### Справочники
- ✅ Управление статусами
- ✅ Управление типами операций
- ✅ Управление категориями (с привязкой к типу)
- ✅ Управление подкатегориями (с привязкой к категории)
- ✅ CRUD через модальные окна (без перезагрузки)
- ✅ Валидация зависимостей (категория → тип, подкатегория → категория)

### Логические зависимости
- ✅ Подкатегории привязаны к категориям
- ✅ Категории привязаны к типам операций
- ✅ Каскадное обновление связанных записей
- ✅ Защита от удаления связанных справочников

### Валидация данных

**Обязательные поля:**
- ✅ Сумма (должна быть > 0)
- ✅ Тип операции
- ✅ Категория
- ✅ Подкатегория

**Уровни валидации:**

| Уровень | Реализация | Что проверяет |
|---------|------------|---------------|
| **Client-side** | JavaScript | Обязательные поля, сумма > 0, связи |
| **Server (Forms)** | Django Forms | Сумма, связи, обязательные поля |
| **Server (API)** | DRF Serializers | Сумма, связи, обязательные поля |
| **Model** | Model.clean() | Сумма > 0 |

**Client-side валидация:**
```javascript
// Проверка обязательных полей
// Проверка суммы > 0
// Проверка связей (категория → тип, подкатегория → категория)
```

**Server-side валидация (Forms):**
```python
def clean_amount(self):
    if amount <= 0:
        raise ValidationError('Сумма должна быть больше 0')

def clean(self):
    # Проверка связи категории и типа
    # Проверка связи подкатегории и категории
```

### Интерфейс
- ✅ Современный дизайн на Bootstrap 5
- ✅ Адаптивная вёрстка (mobile-first)
- ✅ Каскадные фильтры в реальном времени
- ✅ Уведомления об успешных операциях
- ✅ Иконки Font Awesome

---

## 🛠 Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.8+ / Django 4.2 |
| API | Django REST Framework 3.17 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5 / CSS3 / JavaScript |
| CSS Framework | Bootstrap 5.3 |
| Icons | Font Awesome 6.4 |
| Fonts | Google Fonts (Inter) |

---

## 📦 Установка

### Требования
- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Git (для клонирования репозитория)

### Шаг 1: Клонирование репозитория
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd crm_dds
```

### Шаг 2: Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей
```bash
pip install -r requirements.txt
```

---

## ⚙️ Настройка

### Шаг 1: Создание файла .env
Скопируйте файл `.env.example` в `.env`:
```bash
cp .env.example .env
```

### Шаг 2: Настройка переменных окружения

Откройте `.env` и настройте переменные:

**Для разработки (SQLite):**
```bash
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**Для production (PostgreSQL):**
```bash
SECRET_KEY=ваш-секретный-ключ-не-менее-50-символов
DEBUG=False
ALLOWED_HOSTS=ваш-домен.com,www.ваш-домен.com

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=crm_dds_db
DB_USER=postgres
DB_PASSWORD=ваш-пароль
DB_HOST=localhost
DB_PORT=5432
```

### Шаг 3: Генерация SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Шаг 4: Применение миграций
```bash
python manage.py migrate
```

### Шаг 5: Загрузка начальных данных
```bash
python manage.py loaddata dds/fixtures/initial_status.json
python manage.py loaddata dds/fixtures/initial_transactiontype.json
python manage.py loaddata dds/fixtures/initial_category.json
python manage.py loaddata dds/fixtures/initial_subcategory.json
```

### Шаг 6: Создание суперпользователя
```bash
python manage.py createsuperuser
```

---

## 🚀 Запуск

### Режим разработки
```bash
python manage.py runserver
```
Приложение доступно по адресу: http://127.0.0.1:8000/

### Production (с Gunicorn)
```bash
# Установка Gunicorn
pip install gunicorn

# Запуск
gunicorn crm_dds.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Админ-панель
```
http://127.0.0.1:8000/admin/
```

---

## 🧪 Тесты

### Запуск всех тестов
```bash
python manage.py test dds
```

### Запуск с покрытием
```bash
pip install coverage
coverage run --source='.' manage.py test dds
coverage report
coverage html
```

### Статус тестов
- **Всего тестов:** 89
- **DRF API:** 29 (полное покрытие CRUD + фильтрация)
- **Integration Tests:** 11 (полный CRUD цикл через Templates)
- **Views (Templates):** 27 (полное покрытие CRUD)
- **Models:** 18
- **Settings:** 2
- **API Integration:** 2

### Покрытие тестами

**100% покрытие CRUD операций:**
- ✅ CashFlow: Create, Read, Update, Delete, Filter
- ✅ Status: Create, Read, Update, Delete
- ✅ TransactionType: Create, Read, Update, Delete
- ✅ Category: Create, Read, Update, Delete
- ✅ Subcategory: Create, Read, Update, Delete

**Интеграционные тесты проверяют:**
- Полный CRUD цикл через Django Templates
- Валидацию форм на сервере
- Связи между сущностями
- Обработку ошибок

---

## 📁 Структура проекта

```
crm_dds/
├── crm_dds/                      # Основной проект Django
│   ├── __init__.py
│   ├── settings.py               # Настройки проекта
│   ├── urls.py                   # Корневые URL
│   ├── wsgi.py                   # WSGI конфигурация
│   └── asgi.py                   # ASGI конфигурация
│
├── dds/                          # Основное приложение
│   ├── __init__.py
│   ├── models.py                 # Модели данных (Status, TransactionType, Category, Subcategory, CashFlow)
│   ├── views.py                  # Представления (CRUD для CashFlow и справочников)
│   ├── forms.py                  # Формы Django с валидацией
│   ├── urls.py                   # URL приложения
│   ├── admin.py                  # Настройка админ-панели
│   ├── api_views.py              # DRF ViewSets для API
│   ├── api_urls.py               # DRF роутер для API
│   ├── serializers.py            # DRF сериализаторы
│   ├── apps.py
│   │
│   ├── tests/                    # Тесты (89 тестов)
│   │   ├── __init__.py
│   │   ├── test_models.py        # Тесты моделей (18 тестов)
│   │   ├── test_views.py         # Тесты views (27 тестов)
│   │   ├── test_api.py           # Тесты DRF API (29 тестов)
│   │   ├── test_integration.py   # Интеграционные тесты (11 тестов)
│   │   └── test_settings.py      # Тесты настроек (2 теста)
│   │
│   ├── fixtures/                 # Фикстуры (начальные данные)
│   │   ├── initial_status.json
│   │   ├── initial_transactiontype.json
│   │   ├── initial_category.json
│   │   └── initial_subcategory.json
│   │
│   └── migrations/               # Миграции Django
│
├── templates/                    # HTML шаблоны
│   ├── base.html                 # Базовый шаблон (навигация, footer)
│   └── dds/                      # Шаблоны приложения
│       ├── cashflow_list.html           # Список операций ДДС
│       ├── cashflow_form.html           # Форма создания/редактирования
│       ├── cashflow_confirm_delete.html # Подтверждение удаления
│       ├── directories.html             # Страница справочников
│       │
│       ├── status_list.html             # Список статусов
│       ├── status_form.html             # Форма статуса
│       ├── status_confirm_delete.html   # Удаление статуса
│       │
│       ├── transactiontype_list.html          # Список типов операций
│       ├── transactiontype_form.html          # Форма типа операции
│       ├── transactiontype_confirm_delete.html# Удаление типа
│       │
│       ├── category_list.html             # Список категорий
│       ├── category_form.html             # Форма категории
│       ├── category_confirm_delete.html   # Удаление категории
│       │
│       ├── subcategory_list.html          # Список подкатегорий
│       ├── subcategory_form.html          # Форма подкатегории
│       └── subcategory_confirm_delete.html# Удаление подкатегории
│
├── static/                       # Статические файлы
│   └── dds/
│       ├── css/
│       │   └── style.css         # Основные стили (Bootstrap + кастомные)
│       ├── js/
│       │   ├── main.js           # Основные JS функции (утилиты)
│       │   ├── api.js            # API клиент для DRF
│       │   └── directories.js    # CRUD для справочников
│       └── images/               # Изображения
│
├── .env                          # Переменные окружения (НЕ в git!)
├── .env.example                  # Пример переменных окружения
├── .gitignore                    # Игнорируемые файлы
├── requirements.txt              # Зависимости Python
├── manage.py                     # Утилита управления Django
└── README.md                     # Документация
```

---

## 🔌 REST API Документация

### Базовый URL
```
/api/
```

### Endpoints

#### CashFlow (Записи ДДС)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/cashflow/` | Список записей (с фильтрацией) |
| POST | `/api/cashflow/` | Создать запись |
| GET | `/api/cashflow/{id}/` | Получить запись |
| PUT | `/api/cashflow/{id}/` | Обновить запись |
| DELETE | `/api/cashflow/{id}/` | Удалить запись |

**Фильтрация:**
```
GET /api/cashflow/?date_from=2025-01-01&date_to=2025-12-31&status_id=1&transaction_type_id=2
```

#### Status (Статусы)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/statuses/` | Список статусов |
| POST | `/api/statuses/` | Создать статус |
| PUT | `/api/statuses/{id}/` | Обновить статус |
| DELETE | `/api/statuses/{id}/` | Удалить статус |

#### TransactionType (Типы операций)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/transaction-types/` | Список типов |
| POST | `/api/transaction-types/` | Создать тип |
| PUT | `/api/transaction-types/{id}/` | Обновить тип |
| DELETE | `/api/transaction-types/{id}/` | Удалить тип |

#### Categories (Категории)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/categories/` | Список категорий |
| GET | `/api/categories/by_transaction_type/?transaction_type_id=1` | По типу операции |
| POST | `/api/categories/` | Создать категорию |
| PUT | `/api/categories/{id}/` | Обновить категорию |
| DELETE | `/api/categories/{id}/` | Удалить категорию |

#### Subcategories (Подкатегории)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/subcategories/` | Список подкатегорий |
| GET | `/api/subcategories/by_category/?category_id=1` | По категории |
| POST | `/api/subcategories/` | Создать подкатегорию |
| PUT | `/api/subcategories/{id}/` | Обновить подкатегорию |
| DELETE | `/api/subcategories/{id}/` | Удалить подкатегорию |

### Примеры запросов

**Создание записи:**
```json
POST /api/cashflow/
{
    "date": "2025-03-25",
    "status": 1,
    "transaction_type": 2,
    "category": 3,
    "subcategory": 5,
    "amount": 1000,
    "comment": "Оплата услуг"
}
```

**Ответ:**
```json
{
    "id": 1,
    "date": "2025-03-25",
    "status": 1,
    "status_name": "Бизнес",
    "transaction_type": 2,
    "transaction_type_name": "Списание",
    "category": 3,
    "category_name": "Маркетинг",
    "subcategory": 5,
    "subcategory_name": "Avito",
    "amount": "1000.00",
    "comment": "Оплата услуг"
}
```

---

## 🔒 Безопасность

### Что уже реализовано:
- ✅ **CSRF защита** — включена по умолчанию
- ✅ **XSS защита** — Django templates автоматически экранируют вывод
- ✅ **SQL Injection защита** — Django ORM использует параметризованные запросы
- ✅ **Clickjacking защита** — XFrameOptionsMiddleware включён
- ✅ **Секреты в .env** — SECRET_KEY и другие настройки в `.env` (не в git)

### `.env` файл (не попадает в git):
```bash
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### ⚠️ Важно для production:
Если будете выкладывать на боевой сервер:
1. Смените `SECRET_KEY` на новый
2. Установите `DEBUG=False`
3. Настройте `ALLOWED_HOSTS=ваш-домен.com`
4. Включите HTTPS

---

## 🌐 Деплой (опционально)

Для пет-проекта **не требуется**. Если хотите задеплоить:

### Простой вариант (PythonAnywhere):
1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Загрузите проект через Git
3. Установите зависимости: `pip install -r requirements.txt`
4. Настройте Web App в панели управления

### Продвинутый вариант (VPS):
```bash
# Установка
pip install gunicorn
python manage.py collectstatic --noinput

# Запуск
gunicorn crm_dds.wsgi:application --bind 0.0.0.0:8000
```

---

## 📝 Лицензия

MIT License — см. файл [LICENSE](LICENSE) для деталей.

---

## 📞 Контакты

По вопросам обращайтесь: [your-email@example.com]

---

## 🙏 Благодарности

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
