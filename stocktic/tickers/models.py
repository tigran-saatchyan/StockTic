"""This module defines the Ticker model and its associated methods.

Classes:
    Ticker: A Django model representing a stock ticker.
"""

import csv
from io import TextIOWrapper

from custom_utils.common.constants import NULLABLE
from custom_utils.common.mixins import DateFieldsMixin
from django.db import models


class Ticker(DateFieldsMixin, models.Model):
    """A Django model representing a stock ticker.

    Attributes:
        symbol (CharField): The stock symbol.
        name (CharField): The stock name.
        country (CharField): The country of the stock.
        ipo_year (IntegerField): The IPO year of the stock.
        stock_exchange (CharField): The stock exchange.
        sector (CharField): The sector of the stock.
        industry (CharField): The industry of the stock.
        last_sale (CharField): The last sale price.
        net_change (CharField): The net change in price.
        percent_change (CharField): The percent change in price.
        market_cap (CharField): The market capitalization.
        volume (CharField): The trading volume.
    """

    symbol = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Symbol",
        help_text="Stock symbol",
        db_index=True,
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
        db_index=True,
    )
    sector = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Sector",
        help_text="Sector",
        db_index=True,
    )
    industry = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Industry",
        help_text="Industry",
    )
    last_sale = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Last Sale",
        help_text="Last sale price",
    )
    net_change = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Net Change",
        help_text="Net change",
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
        """Create Ticker instances from a CSV file.

        Args:
            csv_file (File): The CSV file containing ticker data.
        """
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
        """Create or update Ticker from API data.

        Args:
            data (dict): A dictionary containing 'symbol', 'name',
                'stock_exchange', and 'last_sale'.

        Returns:
            Ticker: The created or updated Ticker instance.
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
        """Return the string representation of the Ticker instance.

        Returns:
            str: The stock symbol.
        """
        return self.symbol
