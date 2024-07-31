import csv
from io import TextIOWrapper

from django.db import models

from services.common.constants import NULLABLE
from services.common.mixins import DateFieldsMixin


class Ticker(DateFieldsMixin, models.Model):
    symbol = models.CharField(
        max_length=10, unique=True, verbose_name="Symbol",
        help_text="Stock symbol"
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
    sector = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Sector", help_text="Sector"
    )
    industry = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Industry",
        help_text="Industry"
    )

    @classmethod
    def create_from_csv(cls, csv_file):
        file = TextIOWrapper(csv_file.file, encoding="utf-8")
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            symbol, name, country, ipo_year, sector, industry = row

            try:
                ipo_year = int(ipo_year)
            except ValueError:
                ipo_year = None
            ticker = cls(
                symbol=symbol,
                name=name,
                country=country,
                ipo_year=ipo_year,
                sector=sector,
                industry=industry,
            )
            ticker.save()
        file.close()

    def __str__(self):
        return self.symbol
