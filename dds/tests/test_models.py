from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date
from ..models import Status, TransactionType, Category, Subcategory, CashFlow

class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name="Тестовый")
        self.assertEqual(str(status), "Тестовый")
        self.assertEqual(status.name, "Тестовый")

    def test_status_unique_constraint(self):
        Status.objects.create(name="Уникальный")
        with self.assertRaises(IntegrityError):
            Status.objects.create(name="Уникальный")
    
    def test_status_verbose_name(self):
        status = Status.objects.create(name="Тест")
        self.assertEqual(status._meta.verbose_name, "Статус")
        self.assertEqual(status._meta.verbose_name_plural, "Статусы")


class TransactionTypeModelTest(TestCase):
    def test_create_transaction_type(self):
        tt = TransactionType.objects.create(name="Пополнение")
        self.assertEqual(str(tt), "Пополнение")
        self.assertEqual(tt.name, "Пополнение")
    
    def test_transaction_type_unique_constraint(self):
        TransactionType.objects.create(name="Списание")
        with self.assertRaises(IntegrityError):
            TransactionType.objects.create(name="Списание")
    
    def test_transaction_type_verbose_name(self):
        tt = TransactionType.objects.create(name="Тест")
        self.assertEqual(tt._meta.verbose_name, "Тип операции")
        self.assertEqual(tt._meta.verbose_name_plural, "Типы операций")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.type = TransactionType.objects.create(name="Списание")

    def test_category_str(self):
        category = Category.objects.create(name="Маркетинг", transaction_type=self.type)
        self.assertEqual(str(category), "Списание - Маркетинг")

    def test_category_unique_with_type(self):
        Category.objects.create(name="Маркетинг", transaction_type=self.type)
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Маркетинг", transaction_type=self.type)
    
    def test_category_verbose_name(self):
        category = Category.objects.create(name="Тест", transaction_type=self.type)
        self.assertEqual(category._meta.verbose_name, "Категория")
        self.assertEqual(category._meta.verbose_name_plural, "Категории")


class SubcategoryModelTest(TestCase):
    def setUp(self):
        self.type = TransactionType.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type)

    def test_subcategory_str(self):
        sub = Subcategory.objects.create(name="Avito", category=self.category)
        self.assertEqual(str(sub), "Маркетинг - Avito")
    
    def test_subcategory_unique_with_category(self):
        Subcategory.objects.create(name="Тест", category=self.category)
        with self.assertRaises(IntegrityError):
            Subcategory.objects.create(name="Тест", category=self.category)
    
    def test_subcategory_verbose_name(self):
        sub = Subcategory.objects.create(name="Тест", category=self.category)
        self.assertEqual(sub._meta.verbose_name, "Подкатегория")
        self.assertEqual(sub._meta.verbose_name_plural, "Подкатегории")


class CashFlowModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Бизнес")
        self.type_expense = TransactionType.objects.create(name="Списание")
        self.type_income = TransactionType.objects.create(name="Пополнение")
        self.category = Category.objects.create(name="Маркетинг", transaction_type=self.type_expense)
        self.subcategory = Subcategory.objects.create(name="Avito", category=self.category)

    def test_create_valid_cashflow(self):
        cf = CashFlow.objects.create(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            subcategory=self.subcategory,
            amount=1000
        )
        self.assertEqual(cf.amount, 1000)
        self.assertEqual(cf.date, date.today())
    
    def test_cashflow_str(self):
        cf = CashFlow.objects.create(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            amount=1000
        )
        self.assertIn("Маркетинг", str(cf))
        self.assertIn("1000", str(cf))

    def test_amount_must_be_positive(self):
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            amount=-100
        )
        with self.assertRaises(ValidationError) as cm:
            cf.full_clean()
        self.assertIn('amount', cm.exception.message_dict)
    
    def test_amount_zero_invalid(self):
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            amount=0
        )
        with self.assertRaises(ValidationError) as cm:
            cf.full_clean()
        self.assertIn('amount', cm.exception.message_dict)

    def test_category_belongs_to_transaction_type(self):
        """Валидация связи категории и типа выполняется в форме, не в модели"""
        # Модель позволяет создать запись без валидации связей
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_income,
            category=self.category,
            amount=1000
        )
        # В модели проверяется только сумма
        try:
            cf.clean()
        except ValidationError:
            self.fail("Model clean() should not validate category-transaction_type relation")
    
    def test_subcategory_belongs_to_category(self):
        """Валидация связи подкатегории и категории выполняется в форме, не в модели"""
        # Модель позволяет создать запись без валидации связей
        other_category = Category.objects.create(
            name="Инфраструктура", transaction_type=self.type_expense
        )
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_expense,
            category=other_category,
            subcategory=self.subcategory,
            amount=1000
        )
        # В модели проверяется только сумма
        try:
            cf.clean()
        except ValidationError:
            self.fail("Model clean() should not validate subcategory-category relation")

    def test_subcategory_optional(self):
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            amount=1000
        )
        try:
            cf.full_clean()
        except ValidationError:
            self.fail("Subcategory optional should not raise ValidationError")
    
    def test_cashflow_verbose_name(self):
        cf = CashFlow(
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            amount=1000
        )
        self.assertEqual(cf._meta.verbose_name, "Запись ДДС")
        self.assertEqual(cf._meta.verbose_name_plural, "Записи ДДС")
