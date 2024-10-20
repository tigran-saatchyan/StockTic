"""This module defines the views for the tickers app.

Views:
    ticker_list: Renders a list of tickers.
    ticker_detail: Renders the details of a specific ticker.
    export_tickers: Exports tickers to a CSV file.
    import_tickers: Imports tickers from a CSV file.
    get_stock_info: Renders the stock information of a specific ticker.
    get_stock_history: Renders the stock history of a specific ticker.
    search_tickers: Searches for tickers based on a query.
    FetchTickersAsyncView: A view to fetch tickers asynchronously using Celery.
"""

import csv

from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from tickers.tasks import fetch_tickers_from_api

from .models import Ticker
from .services import Finance


def ticker_list(request):
    """Renders a list of tickers.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object containing the rendered template.
    """
    cached_data = cache.get("nasdaq_symbols")

    if not cached_data:
        tickers = Ticker.objects.all()
        cache.set("nasdaq_symbols", tickers, 60 * 60)
    else:
        tickers = cached_data

    return render(
        request,
        "tickers/ticker_list.html",
        {"tickers": tickers, "title": "Nasdaq Symbols"},
    )


def ticker_detail(request, symbol):
    """Renders the details of a specific ticker.

    Args:
        request (HttpRequest): The request object.
        symbol (str): The symbol of the ticker.

    Returns:
        HttpResponse: The response object containing the rendered template.
    """
    ticker = get_object_or_404(Ticker, symbol=symbol)
    return render(request, "tickers/ticker_detail.html", {"ticker": ticker})


def export_tickers(request):
    """Exports tickers to a CSV file.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object containing the CSV file.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tickers.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Symbol", "Name", "Country", "IPO Year", "Sector", "Industry"]
    )

    for ticker in Ticker.objects.all():
        writer.writerow(
            [
                ticker.symbol,
                ticker.name,
                ticker.country,
                ticker.ipo_year,
                ticker.sector,
                ticker.industry,
            ]
        )

    return response


def import_tickers(request):
    """Imports tickers from a CSV file.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object indicating the result of the import.
    """
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        with transaction.atomic():
            Ticker.objects.all().delete()
            Ticker.create_from_csv(csv_file)
        cache.delete("nasdaq_symbols")
        return HttpResponse("CSV file uploaded successfully.")
    return None


def get_stock_info(request, symbol):
    """Renders the stock information of a specific ticker.

    Args:
        request (HttpRequest): The request object.
        symbol (str): The symbol of the ticker.

    Returns:
        HttpResponse: The response object containing the rendered template.
    """
    if request.method == "GET":
        finance = Finance(symbol)
        info = finance.get_info()
        return render(
            request,
            "tickers/company_profile.html",
            {"company_profile": info, "title": info.get("shortName")},
        )
    return None


def get_stock_history(request, symbol):
    """Renders the stock history of a specific ticker.

    Args:
        request (HttpRequest): The request object.
        symbol (str): The symbol of the ticker.

    Returns:
        HttpResponse: The response object containing the rendered template.
    """
    if request.method == "GET":
        finance = Finance(symbol)
        history = finance.get_history()
        return render(
            request,
            "tickers/history.html",
            {"history": history, "title": f"{symbol} History"},
        )
    return None


def search_tickers(request):
    """Searches for tickers based on a query.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: The response object containing the search results.
    """
    query = request.GET.get("q", "")
    if query:
        tickers = Ticker.objects.filter(symbol__icontains=query)[:10]
        results = [{"symbol": ticker.symbol} for ticker in tickers]
    else:
        results = []
    return JsonResponse({"results": results})


class FetchTickersAsyncView(View):
    """A view to fetch tickers asynchronously using Celery.

    Methods:
        post: Starts the Celery task to fetch tickers.
    """

    def post(self, request, *args, **kwargs):
        """Starts the Celery task to fetch tickers.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: The response object indicating the task status.
        """
        fetch_tickers_from_api.delay()
        return JsonResponse(
            {"message": "Tickers fetch started asynchronously!"}, status=202
        )
