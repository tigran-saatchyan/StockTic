"""This module defines serializers for the Ticker model.

Classes:
    TickerSerializer: A serializer for the Ticker model.
"""

from rest_framework import serializers

from .models import Ticker


class TickerSerializer(serializers.ModelSerializer):
    """A serializer for the Ticker model.

    Meta:
        model (Ticker): The model to be serialized.
        fields (str): The fields to be included in the serialization.
    """

    class Meta:
        model = Ticker
        fields = "__all__"
