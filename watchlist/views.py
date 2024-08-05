from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from services.common.utils import format_market_cap
from tickers.models import Ticker
from tickers.services import Finance
from .forms import WatchlistForm, AddTickerForm
from .models import WatchlistTicker, Watchlist


def watchlist_list(request):
    watchlists = Watchlist.objects.all()
    return render(
        request,
        'watchlist/watchlist_list.html',
        {'watchlists': watchlists}
    )


def watchlist_detail(request, pk):
    watchlist = get_object_or_404(Watchlist, pk=pk)
    tickers = watchlist.tickers.all()
    finance_data = []

    for ticker in tickers:
        finance = Finance(ticker.symbol)
        info = finance.get_info()
        history = finance.get_history(period="1d", interval="1m")
        if history is not None:
            history.index = history.index.strftime('%Y-%m-%dT%H:%M:%S')
            history_dict = history.reset_index().to_dict('records')

            current_price = info.get('currentPrice', None)
            previous_close = info.get('previousClose', None)

            # Calculate change and change percentage
            change, change_percent = calculate_change_and_change_percentage(
                current_price, previous_close
            )

            # Ensure all necessary keys are present in the info
            day_low = info.get('dayLow', None)
            day_high = info.get('dayHigh', None)
            year_low = info.get('fiftyTwoWeekLow', None)
            year_high = info.get('fiftyTwoWeekHigh', None)
            market_cap = info.get('marketCap', None)

            # Format the market cap
            formatted_market_cap = format_market_cap(
                market_cap
            ) if market_cap else 'N/A'

            day_range_position, year_range_position = calculate_the_day_and_year_range_position(
                current_price, day_high, day_low, year_high, year_low
            )

            finance_data.append(
                {
                    'info': info,
                    'history': history_dict,
                    'dayRangePosition': day_range_position,
                    'yearRangePosition': year_range_position,
                    'formattedMarketCap': formatted_market_cap,
                    'change': change,
                    'changePercent': change_percent,
                }
            )
        else:
            # Handle the case where there's not enough historical data
            finance_data.append(
                {
                    'info': info,
                    'history': [],
                    'dayRangePosition': None,
                    'yearRangePosition': None,
                    'formattedMarketCap': 'N/A',
                    'change': None,
                    'changePercent': None,
                }
            )

    return render(
        request, 'watchlist/watchlist_detail.html',
        {'watchlist': watchlist, 'finance_data': finance_data}
    )


def calculate_the_day_and_year_range_position(
    current_price, day_high, day_low, year_high, year_low
):
    # Calculate the day range position
    if day_low is not None and day_high is not None and current_price is not None:
        day_range_position = (current_price - day_low) / (
                day_high - day_low) * 100
    else:
        day_range_position = None  # Set to None or a default value if calculation is not possible
    # Calculate the year range position
    if year_low is not None and year_high is not None and current_price is not None:
        year_range_position = (current_price - year_low) / (
                year_high - year_low) * 100
    else:
        year_range_position = None
    return day_range_position, year_range_position


def calculate_change_and_change_percentage(current_price, previous_close):
    if previous_close is not None and current_price is not None:
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100
    else:
        change = None
        change_percent = None
    return change, change_percent


def create_watchlist(request):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('watchlist:watchlist_list')
    else:
        form = WatchlistForm()
    return render(request, 'watchlist/create_watchlist.html', {'form': form})


def add_ticker(request, pk):
    watchlist = get_object_or_404(Watchlist, pk=pk)
    if request.method == 'POST':
        form = AddTickerForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['ticker']
            ticker, _ = Ticker.objects.get_or_create(symbol=symbol)
            WatchlistTicker.objects.create(watchlist=watchlist, ticker=ticker)
            return redirect('watchlist:watchlist_detail', pk=watchlist.pk)
    else:
        form = AddTickerForm()
    return render(
        request, 'watchlist/add_ticker.html',
        {'form': form, 'watchlist': watchlist}
    )


class WatchlistTickerDeleteView(DeleteView):
    model = WatchlistTicker
    template_name = 'watchlist/confirm_delete.html'
    context_object_name = 'watchlist_ticker'

    def get_success_url(self):
        watchlist_pk = self.kwargs['watchlist_pk']
        return reverse_lazy(
            'watchlist:watchlist_detail', kwargs={'pk': watchlist_pk}
            )

    def get_object(self, queryset=None):
        watchlist_pk = self.kwargs['watchlist_pk']
        ticker_symbol = self.kwargs['ticker_symbol']
        return get_object_or_404(
            WatchlistTicker, watchlist_id=watchlist_pk,
            ticker__symbol=ticker_symbol
            )