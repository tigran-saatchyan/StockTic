# historical_data/views.py
from django.shortcuts import render
from .models import HistoricalData
from stocks.models import Stock


def historical_data_view(request, ticker):
    try:
        stock = Stock.objects.get(ticker=ticker)
        data = HistoricalData.objects.filter(stock=stock)
    except Stock.DoesNotExist:
        stock = None
        data = None

    return render(
        request, 'historical_data/historical_data.html',
        {'stock': stock, 'data': data}
        )
