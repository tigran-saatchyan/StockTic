# watchlist/models.py
from django.contrib.auth.models import User
from django.db import models

from services.common.mixins import DateFieldsMixin
from stocks.models import Stock
from tickers.models import Ticker


class Watchlist(DateFieldsMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    tickers = models.ManyToManyField(
        Ticker,
        through='WatchlistTicker',
        related_name='watchlists',
        verbose_name="Tickers"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"


class WatchlistTicker(DateFieldsMixin, models.Model):
    watchlist = models.ForeignKey(
        Watchlist,
        on_delete=models.CASCADE,
        related_name='watchlist_tickers',
        verbose_name="Watchlist"
    )
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.CASCADE,
        related_name='watchlist_tickers',
        verbose_name="Ticker"
    )

    def __str__(self):
        return f"{self.watchlist} - {self.ticker}"

    class Meta:
        unique_together = ['watchlist', 'ticker']
        verbose_name = "Watchlist Ticker"
        verbose_name_plural = "Watchlist Tickers"
