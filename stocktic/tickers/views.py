# tickers/views.py
import csv

from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from tickers.tasks import fetch_tickers_from_api
from .models import Ticker
from .services import Finance


def ticker_list(request):
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
    ticker = get_object_or_404(Ticker, symbol=symbol)
    return render(request, "tickers/ticker_detail.html", {"ticker": ticker})


def export_tickers(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tickers.csv"'

    writer = csv.writer(response)
    writer.writerow(["Symbol", "Name", "Country", "IPO Year", "Sector", "Industry"])

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
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        with transaction.atomic():
            Ticker.objects.all().delete()
            Ticker.create_from_csv(csv_file)
        cache.delete("nasdaq_symbols")
        return HttpResponse("CSV file uploaded successfully.")


def get_stock_info(request, symbol):
    if request.method == "GET":
        finance = Finance(symbol)
        info = finance.get_info()
        return render(
            request,
            "tickers/company_profile.html",
            {"company_profile": info, "title": info.get("shortName")},
        )


def get_stock_history(request, symbol):
    if request.method == "GET":
        finance = Finance(symbol)
        history = finance.get_history()
        return render(
            request,
            "tickers/history.html",
            {"history": history, "title": f"{symbol} History"},
        )


def search_tickers(request):
    query = request.GET.get("q", "")
    if query:
        tickers = Ticker.objects.filter(symbol__icontains=query)[:10]
        results = [{"symbol": ticker.symbol} for ticker in tickers]
    else:
        results = []
    return JsonResponse({"results": results})


class FetchTickersAsyncView(View):
    def post(self, request, *args, **kwargs):
        # Запуск Celery задачи
        fetch_tickers_from_api.delay()
        return JsonResponse(
            {"message": "Tickers fetch started asynchronously!"}, status=202
        )
