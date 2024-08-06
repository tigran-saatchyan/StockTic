from django import forms

from .models import Watchlist, WatchlistTicker


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['name']


class AddTickerForm(forms.ModelForm):

    class Meta:
        model = WatchlistTicker
        fields = ['ticker']

        widgets = {
            'ticker': forms.Select(
                attrs={'class': 'normalize', 'placeholder': 'Ticker Symbol'}
            )
        }
