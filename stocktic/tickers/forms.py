"""This module defines the forms for the tickers app.

Forms:
    TickerForm: A form for creating and updating Ticker instances.
"""

from django import forms

from .models import Ticker


class TickerForm(forms.ModelForm):
    """A form for creating and updating Ticker instances.

    Attributes:
        model (Model): The model associated with the form.
        fields (str): The fields to include in the form.
    """

    class Meta:
        model = Ticker
        fields = "__all__"
