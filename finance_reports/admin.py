from django.contrib import admin

from .models import Category, Income, Expense, Asset, Liability

# Register your models here.

admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Asset)
admin.site.register(Liability)
