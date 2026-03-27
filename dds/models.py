from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']


class TransactionType(models.Model):
    TYPE_COLOR_CHOICES = [
        ('income', 'Пополнение'),
        ('expense', 'Списание'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    type_color = models.CharField(max_length=10, choices=TYPE_COLOR_CHOICES, default='expense', verbose_name="Тип операции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE,
        related_name='categories', verbose_name="Тип операции"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.transaction_type.name} - {self.name}"
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['transaction_type', 'name']
        unique_together = ['name', 'transaction_type']


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='subcategories', verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category', 'name']
        unique_together = ['name', 'category']


class CashFlow(models.Model):
    date = models.DateField(default=date.today, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.PROTECT,
        null=True, blank=True, verbose_name="Подкатегория"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма (₽)")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления записи")
    
    def clean(self):
        # Простая валидация суммы
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({'amount': 'Сумма должна быть больше 0'})
        # Валидация связей выполняется в форме (CashFlowForm.clean())
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount} ₽"
    
    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date', '-created_at']
