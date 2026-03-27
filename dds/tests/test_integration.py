"""
Интеграционные тесты для CRUD операций
Проверяют полный цикл работы через Django Templates (frontend)
"""
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Status, TransactionType, Category, Subcategory, CashFlow


class CashFlowIntegrationTest(TestCase):
    """Полные интеграционные тесты для CashFlow CRUD"""
    
    def setUp(self):
        self.client = Client()
        # Создаём тестовые данные
        self.status = Status.objects.create(name="Бизнес")
        self.type_expense = TransactionType.objects.create(name="Списание")
        self.type_income = TransactionType.objects.create(name="Пополнение")
        self.category_expense = Category.objects.create(
            name="Маркетинг", 
            transaction_type=self.type_expense
        )
        self.category_income = Category.objects.create(
            name="Доход от услуг", 
            transaction_type=self.type_income
        )
        self.subcategory = Subcategory.objects.create(
            name="Avito", 
            category=self.category_expense
        )
    
    def test_full_crud_cycle(self):
        """Тест полного цикла CRUD: Create → Read → Update → Delete"""
        # CREATE: Создание записи через форму
        create_data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category_expense.id,
            'subcategory': self.subcategory.id,
            'amount': 1000,
            'comment': 'Тестовая запись'
        }
        response = self.client.post(reverse('cashflow_create'), create_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем что запись создана
        self.assertEqual(CashFlow.objects.count(), 1)
        cashflow = CashFlow.objects.first()
        self.assertEqual(cashflow.amount, 1000)
        self.assertEqual(cashflow.comment, 'Тестовая запись')
        
        # READ: Чтение записи (главная страница)
        response = self.client.get(reverse('cashflow_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_list.html')
        
        # UPDATE: Обновление записи
        update_data = {
            'date': '2025-03-26',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category_expense.id,
            'subcategory': self.subcategory.id,
            'amount': 2000,
            'comment': 'Обновлено'
        }
        response = self.client.post(reverse('cashflow_update', args=[cashflow.pk]), update_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем обновление
        cashflow.refresh_from_db()
        self.assertEqual(cashflow.amount, 2000)
        self.assertEqual(cashflow.comment, 'Обновлено')
        
        # DELETE: Удаление записи
        response = self.client.post(reverse('cashflow_delete', args=[cashflow.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем удаление
        self.assertEqual(CashFlow.objects.count(), 0)
    
    def test_create_with_income_type(self):
        """Создание записи с типом 'Пополнение'"""
        create_data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_income.id,
            'category': self.category_income.id,
            'amount': 5000,
            'comment': 'Доход'
        }
        response = self.client.post(reverse('cashflow_create'), create_data)
        self.assertEqual(response.status_code, 302)  # Redirect после успешного создания
        
        cashflow = CashFlow.objects.first()
        self.assertEqual(cashflow.transaction_type, self.type_income)
        self.assertEqual(cashflow.amount, 5000)
    
    def test_create_invalid_category_for_type(self):
        """Попытка создать запись с неверной категорией для типа"""
        # Категория для Списание, а Тип указан Пополнение
        create_data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_income.id,  # Пополнение
            'category': self.category_expense.id,  # Категория для Списание
            'amount': 1000
        }
        response = self.client.post(reverse('cashflow_create'), create_data)
        self.assertEqual(response.status_code, 200)  # Форма должна вернуться с ошибкой
        self.assertFormError(response, 'form', 'category', 
                           'Select a valid choice. That choice is not one of the available choices.')
    
    def test_create_invalid_amount(self):
        """Попытка создать запись с отрицательной суммой"""
        create_data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category_expense.id,
            'amount': -100
        }
        response = self.client.post(reverse('cashflow_create'), create_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'amount', 'Сумма должна быть больше 0')
    
    def test_create_zero_amount(self):
        """Попытка создать запись с нулевой суммой"""
        create_data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category_expense.id,
            'amount': 0
        }
        response = self.client.post(reverse('cashflow_create'), create_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'amount', 'Сумма должна быть больше 0')
    
    def test_update_changes(self):
        """Обновление всех полей записи"""
        from decimal import Decimal
        # Создаём запись
        cashflow = CashFlow.objects.create(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category_expense,
            subcategory=self.subcategory,
            amount=1000
        )
        
        # Обновляем
        update_data = {
            'date': '2025-04-01',
            'status': self.status.id,
            'transaction_type': self.type_income.id,
            'category': self.category_income.id,
            'amount': 9999.99,
            'comment': 'Новый комментарий'
        }
        response = self.client.post(
            reverse('cashflow_update', args=[cashflow.pk]), 
            update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        cashflow.refresh_from_db()
        self.assertEqual(str(cashflow.date), '2025-04-01')
        self.assertEqual(cashflow.amount, Decimal('9999.99'))
        self.assertEqual(cashflow.comment, 'Новый комментарий')
    
    def test_delete_confirmation_page(self):
        """Проверка страницы подтверждения удаления"""
        cashflow = CashFlow.objects.create(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category_expense,
            amount=1000
        )
        
        response = self.client.get(reverse('cashflow_delete', args=[cashflow.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_confirm_delete.html')
        self.assertContains(response, cashflow.category.name)


class DirectoryIntegrationTest(TestCase):
    """Интеграционные тесты для CRUD справочников"""
    
    def setUp(self):
        self.client = Client()
        self.type = TransactionType.objects.create(name="Списание")
    
    def test_status_crud_cycle(self):
        """Полный цикл CRUD для Status"""
        # Create
        response = self.client.post(reverse('status_create'), {'name': 'Новый'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 1)  # Было 0, стало 1
        
        # Get created status
        status = Status.objects.get(name='Новый')
        
        # Update
        response = self.client.post(reverse('status_update', args=[status.pk]), 
                                    {'name': 'Обновленный'}, follow=True)
        self.assertEqual(response.status_code, 200)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Обновленный')
        
        # Delete
        response = self.client.post(reverse('status_delete', args=[status.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 0)
    
    def test_transaction_type_crud_cycle(self):
        """Полный цикл CRUD для TransactionType"""
        # Create
        response = self.client.post(reverse('transactiontype_create'), {'name': 'Пополнение'}, follow=True)
        self.assertEqual(TransactionType.objects.count(), 2)
        
        new_type = TransactionType.objects.get(name='Пополнение')
        
        # Update
        response = self.client.post(reverse('transactiontype_update', args=[new_type.pk]), 
                                    {'name': 'Обновлено'}, follow=True)
        new_type.refresh_from_db()
        self.assertEqual(new_type.name, 'Обновлено')
        
        # Delete
        response = self.client.post(reverse('transactiontype_delete', args=[new_type.pk]), follow=True)
        self.assertEqual(TransactionType.objects.count(), 1)
    
    def test_category_with_transaction_type(self):
        """Создание категории с привязкой к типу"""
        # Create
        response = self.client.post(reverse('category_create'), {
            'name': 'Тестовая',
            'transaction_type': self.type.id
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        
        category = Category.objects.first()
        self.assertEqual(category.transaction_type, self.type)
        
        # Update
        response = self.client.post(reverse('category_update', args=[category.pk]), {
            'name': 'Обновленная',
            'transaction_type': self.type.id
        }, follow=True)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Обновленная')
        
        # Delete
        response = self.client.post(reverse('category_delete', args=[category.pk]), follow=True)
        self.assertEqual(Category.objects.count(), 0)
    
    def test_subcategory_with_category(self):
        """Создание подкатегории с привязкой к категории"""
        category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
        
        # Create
        response = self.client.post(reverse('subcategory_create'), {
            'name': 'Avito',
            'category': category.id
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subcategory.objects.count(), 1)
        
        subcategory = Subcategory.objects.first()
        self.assertEqual(subcategory.category, category)
        
        # Update
        response = self.client.post(reverse('subcategory_update', args=[subcategory.pk]), {
            'name': 'Обновлено',
            'category': category.id
        }, follow=True)
        subcategory.refresh_from_db()
        self.assertEqual(subcategory.name, 'Обновлено')
        
        # Delete
        response = self.client.post(reverse('subcategory_delete', args=[subcategory.pk]), follow=True)
        self.assertEqual(Subcategory.objects.count(), 0)
