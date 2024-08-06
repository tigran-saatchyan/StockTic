from django import forms
from .models import Income, Expense, Asset, Liability, Category

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'source']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'value']

class LiabilityForm(forms.ModelForm):
    class Meta:
        model = Liability
        fields = ['name', 'value']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
