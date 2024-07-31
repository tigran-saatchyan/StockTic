from django.shortcuts import render, redirect, get_object_or_404

from tickers.models import Ticker
from tickers.services import Finance
from .forms import WatchlistForm, AddTickerForm
from .models import Watchlist, WatchlistTicker


def watchlist_list(request):
    watchlists = Watchlist.objects.all()
    return render(
        request, 'watchlist/watchlist_list.html', {'watchlists': watchlists}
        )


def watchlist_detail(request, pk):
    watchlist = get_object_or_404(Watchlist, pk=pk)
    tickers = watchlist.tickers.all()
    finance_data = []
    for ticker in tickers:
        finance = Finance(ticker.symbol)
        info = finance.get_info()
        history = finance.get_history(period="1d")
        history.index = history.index.strftime('%Y-%m-%dT%H:%M:%S')
        finance_data.append(
            {
                'info': info,
                'history': history.reset_index().to_dict('records'),
            }
        )
    return render(
        request, 'watchlist/watchlist_detail.html',
        {'watchlist': watchlist, 'finance_data': finance_data}
        )


def create_watchlist(request):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save()
            return redirect('watchlist:watchlist_list')
    else:
        form = WatchlistForm()
    return render(request, 'watchlist/create_watchlist.html', {'form': form})


def add_ticker(request, pk):
    watchlist = get_object_or_404(Watchlist, pk=pk)
    if request.method == 'POST':
        form = AddTickerForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['ticker_symbol']
            ticker, _ = Ticker.objects.get_or_create(symbol=symbol)
            WatchlistTicker.objects.create(watchlist=watchlist, ticker=ticker)
            return redirect('watchlist:watchlist_detail', pk=watchlist.pk)
    else:
        form = AddTickerForm()
    return render(
        request, 'watchlist/add_ticker.html',
        {'form': form, 'watchlist': watchlist}
        )
