"""This module defines the form for the notifications app.

Forms:
    NotificationForm: A form for creating and updating Notification instances.
"""

from typing import ClassVar

from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    """A form for creating and updating Notification instances.

    Meta:
        model (Model): The model associated with the form.
        fields (list): The fields to include in the form.
        widgets (dict): The widgets to use for each field in the form.
    """

    class Meta:
        model = Notification
        fields: ClassVar = [
            "user",
            "ticker",
            "notification_value",
            "notification_type",
            "notification_criteria",
        ]
        widgets: ClassVar = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "ticker": forms.Select(
                attrs={
                    "class": "normalize",
                }
            ),
            "notification_value": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "notification_type": forms.Select(attrs={"class": "normalize"}),
            "notification_criteria": forms.Select(
                attrs={"class": "normalize"}
            ),
        }
