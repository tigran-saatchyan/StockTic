# finance_reports/views.py

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .forms import (
    IncomeForm, ExpenseForm, AssetForm, LiabilityForm, CategoryForm,
)
from .models import Income, Expense, Asset, Liability, Category


def index(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    assets = Asset.objects.all()
    liabilities = Liability.objects.all()
    return render(
        request, 'finance_reports/index.html', {
            'incomes': incomes,
            'expenses': expenses,
            'assets': assets,
            'liabilities': liabilities,
        }
    )


def save_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request
    )
    return JsonResponse(data)


# Income views
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
    else:
        form = IncomeForm()
    return save_form(
        request, form,
        'finance_reports/modals/income/partial_income_create.html'
    )


def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
    else:
        form = IncomeForm(instance=income)
    return save_form(
        request, form,
        'finance_reports/modals/income/partial_income_edit.html'
    )


def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    data = dict()
    if request.method == 'POST':
        income.delete()
        data['form_is_valid'] = True
    else:
        context = {'income': income}
        data['html_form'] = render_to_string(
            'finance_reports/modals/income/partial_income_delete.html',
            context,
            request=request
        )
    return JsonResponse(data)


# Expense views
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm()
    return save_form(
        request, form,
        'finance_reports/modals/expense/partial_expense_create.html'
    )


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
    else:
        form = ExpenseForm(instance=expense)
    return save_form(
        request, form,
        'finance_reports/modals/expense/partial_expense_edit.html'
    )


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    data = dict()
    if request.method == 'POST':
        expense.delete()
        data['form_is_valid'] = True
    else:
        context = {'expense': expense}
        data['html_form'] = render_to_string(
            'finance_reports/modals/expense/partial_expense_delete.html',
            context,
            request=request
        )
    return JsonResponse(data)


# Asset views
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
    else:
        form = AssetForm()
    return save_form(
        request, form,
        'finance_reports/modals/asset/partial_asset_create.html'
    )


def edit_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
    else:
        form = AssetForm(instance=asset)
    return save_form(
        request, form,
        'finance_reports/modals/asset/partial_asset_edit.html'
    )


def delete_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    data = dict()
    if request.method == 'POST':
        asset.delete()
        data['form_is_valid'] = True
    else:
        context = {'asset': asset}
        data['html_form'] = render_to_string(
            'finance_reports/modals/asset/partial_asset_delete.html',
            context,
            request=request
        )
    return JsonResponse(data)


# Liability views
def add_liability(request):
    if request.method == 'POST':
        form = LiabilityForm(request.POST)
    else:
        form = LiabilityForm()
    return save_form(
        request, form,
        'finance_reports/modals/liability/partial_liability_create.html'
    )


def edit_liability(request, pk):
    liability = get_object_or_404(Liability, pk=pk)
    if request.method == 'POST':
        form = LiabilityForm(request.POST, instance=liability)
    else:
        form = LiabilityForm(instance=liability)
    return save_form(
        request, form,
        'finance_reports/modals/liability/partial_liability_edit.html'
    )


def delete_liability(request, pk):
    liability = get_object_or_404(Liability, pk=pk)
    data = dict()
    if request.method == 'POST':
        liability.delete()
        data['form_is_valid'] = True
    else:
        context = {'liability': liability}
        data['html_form'] = render_to_string(
            'finance_reports/modals/liability/partial_liability_delete.html',
            context,
            request=request
        )
    return JsonResponse(data)


def manage_categories(request):
    categories = Category.objects.all()
    return render(
        request, 'finance_reports/manage_categories.html',
        {'categories': categories}
        )


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    else:
        form = CategoryForm()
    return save_form(
        request, form,
        'finance_reports/modals/category/partial_category_create.html'
        )


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
    else:
        form = CategoryForm(instance=category)
    return save_form(
        request, form,
        'finance_reports/modals/category/partial_category_edit.html'
        )


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    data = dict()
    if request.method == 'POST':
        category.delete()
        data['form_is_valid'] = True
    else:
        context = {'category': category}
        data['html_form'] = render_to_string(
            'finance_reports/modals/category/partial_category_delete.html',
            context,
            request=request
        )
    return JsonResponse(data)
