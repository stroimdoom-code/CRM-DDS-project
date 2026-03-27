"""
Тесты для Django Views (Templates)
Покрывают все CRUD операции для справочников и CashFlow
"""
from django.test import TestCase
from django.urls import reverse
from ..models import Status, TransactionType, Category, Subcategory, CashFlow


class CashFlowViewsTest(TestCase):
    """Тесты для CashFlow Views (Templates)"""
    
    def setUp(self):
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
    
    def test_cashflow_list_view_status_code(self):
        """GET / - главная страница"""
        response = self.client.get(reverse('cashflow_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_list.html')
    
    def test_cashflow_create_view_get(self):
        """GET /create/ - страница создания"""
        response = self.client.get(reverse('cashflow_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_form.html')
    
    def test_cashflow_create_view_post_valid(self):
        """POST /create/ - создание записи"""
        data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': 500,
            'comment': 'Тестовая запись'
        }
        response = self.client.post(reverse('cashflow_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CashFlow.objects.count(), 2)
    
    def test_cashflow_create_view_post_invalid(self):
        """POST /create/ - невалидная сумма"""
        data = {
            'date': '2025-03-25',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'amount': -100
        }
        response = self.client.post(reverse('cashflow_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'amount', 'Сумма должна быть больше 0')
    
    def test_cashflow_update_view_get(self):
        """GET /{id}/update/ - страница редактирования"""
        response = self.client.get(reverse('cashflow_update', args=[self.cashflow.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_form.html')
    
    def test_cashflow_update_view_post_valid(self):
        """POST /{id}/update/ - обновление записи"""
        data = {
            'date': '2025-03-26',
            'status': self.status.id,
            'transaction_type': self.type_expense.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': 2000,
            'comment': 'Обновлено'
        }
        response = self.client.post(reverse('cashflow_update', args=[self.cashflow.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.cashflow.refresh_from_db()
        self.assertEqual(self.cashflow.amount, 2000)
    
    def test_cashflow_delete_view_get(self):
        """GET /{id}/delete/ - страница подтверждения удаления"""
        response = self.client.get(reverse('cashflow_delete', args=[self.cashflow.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/cashflow_confirm_delete.html')
    
    def test_cashflow_delete_view_post(self):
        """POST /{id}/delete/ - удаление записи"""
        response = self.client.post(reverse('cashflow_delete', args=[self.cashflow.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CashFlow.objects.count(), 0)


class StatusViewsTest(TestCase):
    """Тесты для Status Views (Templates)"""
    
    def setUp(self):
        self.status = Status.objects.create(name="Тестовый")
    
    def test_status_list_view(self):
        """GET /status/ - список статусов"""
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/status_list.html')
    
    def test_status_create_view_get(self):
        """GET /status/create/ - страница создания"""
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/status_form.html')
    
    def test_status_create_view_post_valid(self):
        """POST /status/create/ - создание статуса"""
        response = self.client.post(reverse('status_create'), {'name': 'Новый статус'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)
    
    def test_status_update_view_get(self):
        """GET /status/{id}/update/ - страница редактирования"""
        response = self.client.get(reverse('status_update', args=[self.status.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/status_form.html')
    
    def test_status_update_view_post_valid(self):
        """POST /status/{id}/update/ - обновление статуса"""
        response = self.client.post(reverse('status_update', args=[self.status.pk]), 
                                    {'name': 'Обновленный'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный')
    
    def test_status_delete_view_get(self):
        """GET /status/{id}/delete/ - страница подтверждения"""
        response = self.client.get(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/status_confirm_delete.html')
    
    def test_status_delete_view_post(self):
        """POST /status/{id}/delete/ - удаление статуса"""
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)


class TransactionTypeViewsTest(TestCase):
    """Тесты для TransactionType Views (Templates)"""
    
    def setUp(self):
        self.type = TransactionType.objects.create(name="Списание")
    
    def test_transactiontype_list_view(self):
        """GET /transactiontype/ - список типов"""
        response = self.client.get(reverse('transactiontype_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/transactiontype_list.html')
    
    def test_transactiontype_create_view_post_valid(self):
        """POST /transactiontype/create/ - создание типа"""
        response = self.client.post(reverse('transactiontype_create'), {'name': 'Пополнение'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TransactionType.objects.count(), 2)
    
    def test_transactiontype_update_view_post_valid(self):
        """POST /transactiontype/{id}/update/ - обновление типа"""
        response = self.client.post(reverse('transactiontype_update', args=[self.type.pk]), 
                                    {'name': 'Обновлено'})
        self.assertEqual(response.status_code, 302)
        self.type.refresh_from_db()
        self.assertEqual(self.type.name, 'Обновлено')
    
    def test_transactiontype_delete_view_post(self):
        """POST /transactiontype/{id}/delete/ - удаление типа"""
        response = self.client.post(reverse('transactiontype_delete', args=[self.type.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TransactionType.objects.count(), 0)


class CategoryViewsTest(TestCase):
    """Тесты для Category Views (Templates)"""
    
    def setUp(self):
        self.type = TransactionType.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
    
    def test_category_list_view(self):
        """GET /category/ - список категорий"""
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/category_list.html')
    
    def test_category_create_view_post_valid(self):
        """POST /category/create/ - создание категории"""
        response = self.client.post(reverse('category_create'), 
                                    {'name': 'Новая', 'transaction_type': self.type.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 2)
    
    def test_category_update_view_post_valid(self):
        """POST /category/{id}/update/ - обновление категории"""
        response = self.client.post(reverse('category_update', args=[self.category.pk]), 
                                    {'name': 'Обновлена', 'transaction_type': self.type.id})
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Обновлена')
    
    def test_category_delete_view_post(self):
        """POST /category/{id}/delete/ - удаление категории"""
        response = self.client.post(reverse('category_delete', args=[self.category.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 0)


class SubcategoryViewsTest(TestCase):
    """Тесты для Subcategory Views (Templates)"""
    
    def setUp(self):
        self.type = TransactionType.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
        self.subcategory = Subcategory.objects.create(name="Avito", category=self.category)
    
    def test_subcategory_list_view(self):
        """GET /subcategory/ - список подкатегорий"""
        response = self.client.get(reverse('subcategory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/subcategory_list.html')
    
    def test_subcategory_create_view_post_valid(self):
        """POST /subcategory/create/ - создание подкатегории"""
        response = self.client.post(reverse('subcategory_create'), 
                                    {'name': 'Новая', 'category': self.category.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Subcategory.objects.count(), 2)
    
    def test_subcategory_update_view_post_valid(self):
        """POST /subcategory/{id}/update/ - обновление подкатегории"""
        response = self.client.post(reverse('subcategory_update', args=[self.subcategory.pk]), 
                                    {'name': 'Обновлена', 'category': self.category.id})
        self.assertEqual(response.status_code, 302)
        self.subcategory.refresh_from_db()
        self.assertEqual(self.subcategory.name, 'Обновлена')
    
    def test_subcategory_delete_view_post(self):
        """POST /subcategory/{id}/delete/ - удаление подкатегории"""
        response = self.client.post(reverse('subcategory_delete', args=[self.subcategory.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Subcategory.objects.count(), 0)
