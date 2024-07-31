# dashboard/views.py
from django.shortcuts import render

from portfolio.models import Portfolio
from stocks.models import Stock


def dashboard_view(request):
    # Пример получения данных для отчетов
    stocks = Stock.objects.all()
    portfolios = Portfolio.objects.all()

    return render(
        request, 'dashboard/dashboard.html', {
            'stocks': stocks,
            'portfolios': portfolios,
        }
    )
