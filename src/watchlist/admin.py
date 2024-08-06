from django.contrib import admin

# Register your models here.

from .models import Watchlist, WatchlistTicker

admin.site.register(Watchlist)
admin.site.register(WatchlistTicker)
