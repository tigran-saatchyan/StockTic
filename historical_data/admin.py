from django.contrib import admin

# Register your models here.

from .models import HistoricalData

admin.site.register(HistoricalData)