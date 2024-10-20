"""This module registers the Ticker model with the Django admin interface.

Classes:
    TickerAdmin: Custom admin interface for the Ticker model.
"""

from django.contrib import admin

from .forms import TickerForm
from .models import Ticker


class TickerAdmin(admin.ModelAdmin):
    """Custom admin interface for the Ticker model.

    Attributes:
        form (ModelForm): The form class to use for the admin interface.
        fieldsets (tuple): The fieldsets to use in the admin interface.
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
    """

    form = TickerForm
    fieldsets = (
        (None, {"fields": ("symbol", "name")}),
        (
            "Additional Information",
            {"fields": ("country", "ipo_year", "sector", "industry")},
        ),
    )
    list_display = (
        "symbol",
        "name",
        "country",
        "ipo_year",
        "sector",
        "industry",
    )
    search_fields = ("symbol", "name", "country", "sector", "industry")


admin.site.register(Ticker, TickerAdmin)
