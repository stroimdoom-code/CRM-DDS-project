from rest_framework import serializers
from .models import Status, TransactionType, Category, Subcategory, CashFlow


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для Status"""
    class Meta:
        model = Status
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TransactionTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для TransactionType"""
    class Meta:
        model = TransactionType
        fields = ['id', 'name', 'type_color', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Category"""
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'transaction_type', 'transaction_type_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Subcategory"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CashFlowSerializer(serializers.ModelSerializer):
    """Сериализатор для CashFlow с вложенными данными"""
    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = CashFlow
        fields = [
            'id', 'date', 'status', 'status_name',
            'transaction_type', 'transaction_type_name',
            'category', 'category_name',
            'subcategory', 'subcategory_name',
            'amount', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Валидация суммы: должна быть > 0"""
        if value is None or value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше 0")
        return value
    
    def validate(self, data):
        """Валидация связей между сущностями"""
        # Проверка связи категории и типа операции
        if 'category' in data and 'transaction_type' in data:
            category = data['category']
            transaction_type = data['transaction_type']
            # Получаем ID категории и типа для сравнения
            category_id = category.id if hasattr(category, 'id') else category
            type_id = transaction_type.id if hasattr(transaction_type, 'id') else transaction_type
            
            # Проверяем связь через БД
            from .models import Category
            try:
                cat = Category.objects.select_related('transaction_type').get(pk=category_id)
                if cat.transaction_type_id != type_id:
                    raise serializers.ValidationError({
                        'category': f"Категория '{cat.name}' не относится к выбранному типу операции"
                    })
            except Category.DoesNotExist:
                raise serializers.ValidationError({
                    'category': "Выбранная категория не существует"
                })

        # Проверка связи подкатегории и категории
        if 'subcategory' in data and data.get('subcategory'):
            subcategory = data['subcategory']
            category = data.get('category')
            
            if category:
                subcategory_id = subcategory.id if hasattr(subcategory, 'id') else subcategory
                category_id = category.id if hasattr(category, 'id') else category
                
                from .models import Subcategory
                try:
                    sub = Subcategory.objects.select_related('category').get(pk=subcategory_id)
                    if sub.category_id != category_id:
                        raise serializers.ValidationError({
                            'subcategory': f"Подкатегория '{sub.name}' не относится к выбранной категории"
                        })
                except Subcategory.DoesNotExist:
                    raise serializers.ValidationError({
                        'subcategory': "Выбранная подкатегория не существует"
                    })

        return data
