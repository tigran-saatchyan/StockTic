from django import forms

from .models import Watchlist


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['name']


class AddTickerForm(forms.Form):
    ticker_symbol = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'id_ticker_symbol',
            }
        )
    )
