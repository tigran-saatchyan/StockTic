from django.contrib import admin

# Register your models here.

from .models import Portfolio, Transaction

admin.site.register(Portfolio)
admin.site.register(Transaction)
