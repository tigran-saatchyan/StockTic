"""This module provides API viewsets for the notifications app.

ViewSets:
    NotificationViewSet: A viewset for viewing and editing notification
        instances.
"""

from typing import ClassVar

from rest_framework import viewsets

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing notification instances.

    Attributes:
        queryset (QuerySet): The queryset of Notification objects.
        serializer_class (Serializer): The serializer class for
            Notification objects.
        http_method_names (list): The allowed HTTP methods for the viewset.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    http_method_names: ClassVar = ["get", "post", "put", "patch", "delete"]
