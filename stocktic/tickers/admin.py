from django.contrib import admin

from .forms import TickerForm
from .models import Ticker


class TickerAdmin(admin.ModelAdmin):
    form = TickerForm
    fieldsets = (
        (None, {"fields": ("symbol", "name")}),
        (
            "Additional Information",
            {"fields": ("country", "ipo_year", "sector", "industry")},
        ),
    )
    list_display = ("symbol", "name", "country", "ipo_year", "sector", "industry")
    search_fields = ("symbol", "name", "country", "sector", "industry")


admin.site.register(Ticker, TickerAdmin)
