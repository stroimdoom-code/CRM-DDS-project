from django.urls import path
from . import views

urlpatterns = [
    path('', views.cashflow_list, name='cashflow_list'),
    path('create/', views.cashflow_create, name='cashflow_create'),
    path('<int:pk>/update/', views.cashflow_update, name='cashflow_update'),
    path('<int:pk>/delete/', views.cashflow_delete, name='cashflow_delete'),
    path('directories/', views.directories, name='directories'),
    
    # Status CRUD (Templates)
    path('status/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/<int:pk>/update/', views.status_update, name='status_update'),
    path('status/<int:pk>/delete/', views.status_delete, name='status_delete'),
    
    # TransactionType CRUD (Templates)
    path('transactiontype/', views.transactiontype_list, name='transactiontype_list'),
    path('transactiontype/create/', views.transactiontype_create, name='transactiontype_create'),
    path('transactiontype/<int:pk>/update/', views.transactiontype_update, name='transactiontype_update'),
    path('transactiontype/<int:pk>/delete/', views.transactiontype_delete, name='transactiontype_delete'),
    
    # Category CRUD (Templates)
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/update/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Subcategory CRUD (Templates)
    path('subcategory/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategory/<int:pk>/update/', views.subcategory_update, name='subcategory_update'),
    path('subcategory/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),
]
