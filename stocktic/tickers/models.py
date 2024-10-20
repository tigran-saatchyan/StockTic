import csv
from io import TextIOWrapper

from django.db import models

from custom_utils.common.constants import NULLABLE
from custom_utils.common.mixins import DateFieldsMixin


class Ticker(DateFieldsMixin, models.Model):
    symbol = models.CharField(
        max_length=255, unique=True, verbose_name="Symbol", help_text="Stock symbol"
    )
    name = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Name", help_text="Stock name"
    )
    country = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Country", help_text="Country"
    )
    ipo_year = models.IntegerField(
        **NULLABLE, verbose_name="IPO Year", help_text="IPO year"
    )
    stock_exchange = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Stock Exchange",
        help_text="Stock exchange",
    )
    sector = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Sector", help_text="Sector"
    )
    industry = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Industry", help_text="Industry"
    )
    last_sale = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Last Sale", help_text="Last sale price"
    )
    net_change = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Net Change", help_text="Net change"
    )
    percent_change = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Percent Change",
        help_text="Percent change",
    )
    market_cap = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Market Cap",
        help_text="Market capitalization",
    )
    volume = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Volume", help_text="Volume"
    )

    @classmethod
    def create_from_csv(cls, csv_file):
        file = TextIOWrapper(csv_file.file, encoding="utf-8")
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            (
                symbol,
                name,
                last_sale,
                net_change,
                percent_change,
                market_cap,
                country,
                ipo_year,
                volume,
                sector,
                industry,
            ) = row

            try:
                ipo_year = int(ipo_year)
            except ValueError:
                ipo_year = None
            ticker = cls(
                symbol=symbol,
                name=name,
                last_sale=last_sale,
                net_change=net_change,
                percent_change=percent_change,
                market_cap=market_cap,
                country=country,
                ipo_year=ipo_year,
                volume=volume,
                sector=sector,
                industry=industry,
            )
            ticker.save()
        file.close()

    @classmethod
    def create_or_update_from_api(cls, data):
        """
        Create or update Ticker from API data.
        :param data: dict containing 'symbol', 'name', 'stock_exchange', and 'last_sale'
        """
        symbol = data.get("symbol")
        name = data.get("name")
        stock_exchange = data.get("exchange")
        last_sale = data.get("price")

        ticker, _ = cls.objects.update_or_create(
            symbol=symbol,
            defaults={
                "name": name,
                "stock_exchange": stock_exchange,
                "last_sale": last_sale,
            },
        )
        return ticker

    def __str__(self):
        return self.symbol
