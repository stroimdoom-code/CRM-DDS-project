from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    StatusViewSet,
    TransactionTypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    CashFlowViewSet
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'cashflow', CashFlowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
