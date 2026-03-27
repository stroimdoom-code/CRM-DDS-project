from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CashFlow, Status, TransactionType, Category, Subcategory
from .forms import CashFlowForm, StatusForm, TransactionTypeForm, CategoryForm, SubcategoryForm


def cashflow_list(request):
    """Представление списка операций ДДС с фильтрами"""
    queryset = CashFlow.objects.select_related(
        'status', 'transaction_type', 'category', 'subcategory'
    ).all()
    
    # Фильтрация
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('transaction_type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if status_id:
        queryset = queryset.filter(status_id=status_id)
    if type_id:
        queryset = queryset.filter(transaction_type_id=type_id)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if subcategory_id:
        queryset = queryset.filter(subcategory_id=subcategory_id)
    
    context = {
        'object_list': queryset,
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'filters': request.GET,
    }
    return render(request, 'dds/cashflow_list.html', context)


def cashflow_create(request):
    """Создание новой записи CashFlow"""
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана')
            return redirect('cashflow_list')
    else:
        form = CashFlowForm()
    
    return render(request, 'dds/cashflow_form.html', {'form': form})


def cashflow_update(request, pk):
    """Редактирование записи CashFlow"""
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена')
            return redirect('cashflow_list')
    else:
        form = CashFlowForm(instance=cashflow)
    
    return render(request, 'dds/cashflow_form.html', {'form': form})


def cashflow_delete(request, pk):
    """Удаление записи CashFlow"""
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cashflow.delete()
        messages.success(request, 'Запись успешно удалена')
        return redirect('cashflow_list')
    
    return render(request, 'dds/cashflow_confirm_delete.html', {'object': cashflow})


def directories(request):
    """Представление страницы справочников"""
    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.select_related('transaction_type').all(),
        'subcategories': Subcategory.objects.select_related('category').all(),
    }
    return render(request, 'dds/directories.html', context)


# ==========================================
# CRUD для справочников (Django Templates)
# ==========================================

# Status CRUD
def status_list(request):
    """Список статусов"""
    objects = Status.objects.all()
    return render(request, 'dds/status_list.html', {'object_list': objects})


def status_create(request):
    """Создание статуса"""
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус создан')
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'dds/status_form.html', {'form': form})


def status_update(request, pk):
    """Редактирование статуса"""
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус обновлен')
            return redirect('status_list')
    else:
        form = StatusForm(instance=obj)
    return render(request, 'dds/status_form.html', {'form': form})


def status_delete(request, pk):
    """Удаление статуса"""
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Статус удален')
        except Exception:
            messages.error(request, 'Невозможно удалить: есть связанные записи')
        return redirect('status_list')
    return render(request, 'dds/status_confirm_delete.html', {'object': obj})


# TransactionType CRUD
def transactiontype_list(request):
    """Список типов операций"""
    objects = TransactionType.objects.all()
    return render(request, 'dds/transactiontype_list.html', {'object_list': objects})


def transactiontype_create(request):
    """Создание типа операции"""
    if request.method == 'POST':
        form = TransactionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип операции создан')
            return redirect('transactiontype_list')
    else:
        form = TransactionTypeForm()
    return render(request, 'dds/transactiontype_form.html', {'form': form})


def transactiontype_update(request, pk):
    """Редактирование типа операции"""
    obj = get_object_or_404(TransactionType, pk=pk)
    if request.method == 'POST':
        form = TransactionTypeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип операции обновлен')
            return redirect('transactiontype_list')
    else:
        form = TransactionTypeForm(instance=obj)
    return render(request, 'dds/transactiontype_form.html', {'form': form})


def transactiontype_delete(request, pk):
    """Удаление типа операции"""
    obj = get_object_or_404(TransactionType, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Тип операции удален')
        except Exception:
            messages.error(request, 'Невозможно удалить: есть связанные записи')
        return redirect('transactiontype_list')
    return render(request, 'dds/transactiontype_confirm_delete.html', {'object': obj})


# Category CRUD
def category_list(request):
    """Список категорий"""
    objects = Category.objects.select_related('transaction_type').all()
    return render(request, 'dds/category_list.html', {'object_list': objects})


def category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория создана')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dds/category_form.html', {'form': form})


def category_update(request, pk):
    """Редактирование категории"""
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория обновлена')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=obj)
    return render(request, 'dds/category_form.html', {'form': form})


def category_delete(request, pk):
    """Удаление категории"""
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Категория удалена')
        except Exception:
            messages.error(request, 'Невозможно удалить: есть связанные записи')
        return redirect('category_list')
    return render(request, 'dds/category_confirm_delete.html', {'object': obj})


# Subcategory CRUD
def subcategory_list(request):
    """Список подкатегорий"""
    objects = Subcategory.objects.select_related('category').all()
    return render(request, 'dds/subcategory_list.html', {'object_list': objects})


def subcategory_create(request):
    """Создание подкатегории"""
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория создана')
            return redirect('subcategory_list')
    else:
        form = SubcategoryForm()
    return render(request, 'dds/subcategory_form.html', {'form': form})


def subcategory_update(request, pk):
    """Редактирование подкатегории"""
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория обновлена')
            return redirect('subcategory_list')
    else:
        form = SubcategoryForm(instance=obj)
    return render(request, 'dds/subcategory_form.html', {'form': form})


def subcategory_delete(request, pk):
    """Удаление подкатегории"""
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Подкатегория удалена')
        except Exception:
            messages.error(request, 'Невозможно удалить: есть связанные записи')
        return redirect('subcategory_list')
    return render(request, 'dds/subcategory_confirm_delete.html', {'object': obj})
