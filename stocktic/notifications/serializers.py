"""This module defines the serializers for the notifications app.

Serializers:
    NotificationSerializer: A serializer for Notification instances.
"""

from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """A serializer for Notification instances.

    Meta:
        model (Model): The model associated with the serializer.
        fields (str): The fields to include in the serializer.
    """

    class Meta:
        model = Notification
        fields = "__all__"
