"""
Тесты для DRF API
Покрывают все CRUD операции для API endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Status, TransactionType, Category, Subcategory, CashFlow


class StatusAPITest(TestCase):
    """Тесты для Status API"""
    
    def setUp(self):
        self.client = APIClient()
        self.status = Status.objects.create(name="Тестовый")
    
    def test_list_statuses(self):
        """GET /api/statuses/ - список статусов"""
        response = self.client.get(reverse('status-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_status(self):
        """POST /api/statuses/ - создание статуса"""
        data = {'name': 'Новый статус'}
        response = self.client.post(reverse('status-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
    
    def test_get_status(self):
        """GET /api/statuses/{id}/ - получение статуса"""
        response = self.client.get(reverse('status-detail', args=[self.status.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Тестовый')
    
    def test_update_status(self):
        """PUT /api/statuses/{id}/ - обновление статуса"""
        data = {'name': 'Обновленный'}
        response = self.client.put(reverse('status-detail', args=[self.status.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный')
    
    def test_delete_status(self):
        """DELETE /api/statuses/{id}/ - удаление статуса"""
        response = self.client.delete(reverse('status-detail', args=[self.status.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 0)


class TransactionTypeAPITest(TestCase):
    """Тесты для TransactionType API"""
    
    def setUp(self):
        self.client = APIClient()
        self.type = TransactionType.objects.create(name="Списание")
    
    def test_list_transaction_types(self):
        """GET /api/transaction-types/ - список типов"""
        response = self.client.get(reverse('transactiontype-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_transaction_type(self):
        """POST /api/transaction-types/ - создание типа"""
        data = {'name': 'Пополнение'}
        response = self.client.post(reverse('transactiontype-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_transaction_type(self):
        """PUT /api/transaction-types/{id}/ - обновление типа"""
        data = {'name': 'Обновлено'}
        response = self.client.put(reverse('transactiontype-detail', args=[self.type.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.type.refresh_from_db()
        self.assertEqual(self.type.name, 'Обновлено')
    
    def test_delete_transaction_type(self):
        """DELETE /api/transaction-types/{id}/ - удаление типа"""
        response = self.client.delete(reverse('transactiontype-detail', args=[self.type.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CategoryAPITest(TestCase):
    """Тесты для Category API"""
    
    def setUp(self):
        self.client = APIClient()
        self.type = TransactionType.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
    
    def test_list_categories(self):
        """GET /api/categories/ - список категорий"""
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_categories_by_transaction_type(self):
        """GET /api/categories/by_transaction_type/ - фильтр по типу"""
        response = self.client.get(
            reverse('category-by-transaction-type'),
            {'transaction_type_id': self.type.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Маркетинг')
    
    def test_create_category(self):
        """POST /api/categories/ - создание категории"""
        data = {'name': 'Новая', 'transaction_type': self.type.id}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_category(self):
        """PUT /api/categories/{id}/ - обновление категории"""
        data = {'name': 'Обновлена', 'transaction_type': self.type.id}
        response = self.client.put(reverse('category-detail', args=[self.category.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Обновлена')
    
    def test_delete_category(self):
        """DELETE /api/categories/{id}/ - удаление категории"""
        response = self.client.delete(reverse('category-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubcategoryAPITest(TestCase):
    """Тесты для Subcategory API"""
    
    def setUp(self):
        self.client = APIClient()
        self.type = TransactionType.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
        self.subcategory = Subcategory.objects.create(name="Avito", category=self.category)
    
    def test_list_subcategories(self):
        """GET /api/subcategories/ - список подкатегорий"""
        response = self.client.get(reverse('subcategory-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_subcategories_by_category(self):
        """GET /api/subcategories/by_category/ - фильтр по категории"""
        response = self.client.get(
            reverse('subcategory-by-category'),
            {'category_id': self.category.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_subcategory(self):
        """POST /api/subcategories/ - создание подкатегории"""
        data = {'name': 'Новая', 'category': self.category.id}
        response = self.client.post(reverse('subcategory-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_subcategory(self):
        """PUT /api/subcategories/{id}/ - обновление подкатегории"""
        data = {'name': 'Обновлена', 'category': self.category.id}
        response = self.client.put(reverse('subcategory-detail', args=[self.subcategory.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_subcategory(self):
        """DELETE /api/subcategories/{id}/ - удаление подкатегории"""
        response = self.client.delete(reverse('subcategory-detail', args=[self.subcategory.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CashFlowAPITest(TestCase):
    """Тесты для CashFlow API"""
    
    def setUp(self):
        self.client = APIClient()
        self.status = Status.objects.create(name="Бизнес")
        self.type_expense = TransactionType.objects.create(name="Списание")
        self.type_income = TransactionType.objects.create(name="Пополнение")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type_expense)
        self.subcategory = Subcategory.objects.create(name="Avito", category=self.category)
        
        self.cashflow = CashFlow.objects.create(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            subcategory=self.subcategory,
            amount=1000
        )
    
    def test_list_cashflow(self):
        """GET /api/cashflow/ - список записей"""
        response = self.client.get(reverse('cashflow-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cashflow_filter_by_status(self):
        """GET /api/cashflow/?status_id=X - фильтр по статусу"""
        response = self.client.get(
            reverse('cashflow-list'),
            {'status_id': self.status.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cashflow_filter_by_transaction_type(self):
        """GET /api/cashflow/?transaction_type_id=X - фильтр по типу"""
        response = self.client.get(
            reverse('cashflow-list'),
            {'transaction_type_id': self.type_expense.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cashflow_filter_by_category(self):
        """GET /api/cashflow/?category_id=X - фильтр по категории"""
        response = self.client.get(
            reverse('cashflow-list'),
            {'category_id': self.category.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cashflow_filter_by_date_range(self):
        """GET /api/cashflow/?date_from=X&date_to=Y - фильтр по датам"""
        # Запись создана с today, поэтому фильтруем с сегодня
        from datetime import date, timedelta
        today = date.today()
        response = self.client.get(
            reverse('cashflow-list'),
            {'date_from': str(today - timedelta(days=1)), 'date_to': str(today + timedelta(days=1))}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_cashflow(self):
        """POST /api/cashflow/ - создание записи"""
        data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': 500,
            'comment': 'Тестовая запись'
        }
        response = self.client.post(reverse('cashflow-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CashFlow.objects.count(), 2)
    
    def test_create_cashflow_invalid_amount(self):
        """POST /api/cashflow/ - валидация суммы"""
        data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'amount': -100  # Неверная сумма
        }
        response = self.client.post(reverse('cashflow-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
    
    def test_get_cashflow(self):
        """GET /api/cashflow/{id}/ - получение записи"""
        response = self.client.get(reverse('cashflow-detail', args=[self.cashflow.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '1000.00')
    
    def test_update_cashflow(self):
        """PUT /api/cashflow/{id}/ - обновление записи"""
        data = {
            'date': '2025-03-26',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': 2000,
            'comment': 'Обновлено'
        }
        response = self.client.put(reverse('cashflow-detail', args=[self.cashflow.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cashflow.refresh_from_db()
        self.assertEqual(self.cashflow.amount, 2000)
    
    def test_delete_cashflow(self):
        """DELETE /api/cashflow/{id}/ - удаление записи"""
        response = self.client.delete(reverse('cashflow-detail', args=[self.cashflow.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CashFlow.objects.count(), 0)
