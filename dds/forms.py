from django import forms
from django.db import models
from .models import CashFlow, Category, Subcategory, Status, TransactionType

class CashFlowForm(forms.ModelForm):
    """Форма для создания и редактирования записей CashFlow"""

    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_transaction_type'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтрация категорий по типу
        if 'transaction_type' in self.data:
            try:
                type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(transaction_type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                transaction_type=self.instance.transaction_type
            )

        # Фильтрация подкатегорий по категории
        if 'category' in self.data:
            try:
                cat_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=cat_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            # При редактировании - показываем только подкатегории этой категории + текущую
            current_subcategory = self.instance.subcategory
            if current_subcategory:
                # Включаем текущую подкатегорию чтобы Django мог её отрендерить
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    models.Q(category=self.instance.category) | models.Q(pk=current_subcategory.pk)
                ).distinct()
            else:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            # Пустой queryset если категория не выбрана
            self.fields['subcategory'].queryset = Subcategory.objects.none()

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError('Сумма должна быть больше 0')
        if amount <= 0:
            raise forms.ValidationError('Сумма должна быть больше 0')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        transaction_type = cleaned_data.get('transaction_type')
        subcategory = cleaned_data.get('subcategory')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise forms.ValidationError(
                    f'Категория "{category.name}" не относится к типу "{transaction_type.name}"'
                )

        if subcategory and category:
            if subcategory.category != category:
                raise forms.ValidationError(
                    f'Подкатегория "{subcategory.name}" не относится к категории "{category.name}"'
                )

        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для справочника Status"""
    class Meta:
        model = Status
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class TransactionTypeForm(forms.ModelForm):
    """Форма для справочника TransactionType"""
    class Meta:
        model = TransactionType
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class CategoryForm(forms.ModelForm):
    """Форма для справочника Category"""
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'})
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для справочника Subcategory"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }
