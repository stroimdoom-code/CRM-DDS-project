from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Status, TransactionType, Category, Subcategory, CashFlow
from .serializers import (
    StatusSerializer,
    TransactionTypeSerializer,
    CategorySerializer,
    SubcategorySerializer,
    CashFlowSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    """API для Status CRUD"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TransactionTypeViewSet(viewsets.ModelViewSet):
    """API для TransactionType CRUD"""
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """API для Category CRUD"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=False, methods=['get'])
    def by_transaction_type(self, request):
        """Получить категории по типу операции"""
        transaction_type_id = request.query_params.get('transaction_type_id')
        if transaction_type_id:
            categories = Category.objects.filter(transaction_type_id=transaction_type_id)
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        return Response([])


class SubcategoryViewSet(viewsets.ModelViewSet):
    """API для Subcategory CRUD"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить подкатегории по категории"""
        category_id = request.query_params.get('category_id')
        if category_id:
            subcategories = Subcategory.objects.filter(category_id=category_id)
            serializer = self.get_serializer(subcategories, many=True)
            return Response(serializer.data)
        return Response([])


class CashFlowViewSet(viewsets.ModelViewSet):
    """API для CashFlow CRUD"""
    queryset = CashFlow.objects.select_related(
        'status', 'transaction_type', 'category', 'subcategory'
    ).all()
    serializer_class = CashFlowSerializer
    
    def get_queryset(self):
        """Фильтрация записей"""
        queryset = super().get_queryset()
        
        # Фильтр по дате (с)
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        # Фильтр по дате (по)
        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        # Фильтр по статусу
        status_id = self.request.query_params.get('status_id')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        
        # Фильтр по типу операции
        transaction_type_id = self.request.query_params.get('transaction_type_id')
        if transaction_type_id:
            queryset = queryset.filter(transaction_type_id=transaction_type_id)
        
        # Фильтр по категории
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтр по подкатегории
        subcategory_id = self.request.query_params.get('subcategory_id')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset
