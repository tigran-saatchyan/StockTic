from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = [
            "user",
            "ticker",
            "notification_value",
            "notification_type",
            "notification_criteria",
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "ticker": forms.Select(
                attrs={
                    "class": "normalize",
                }
            ),
            "notification_value": forms.NumberInput(attrs={"class": "form-control"}),
            "notification_type": forms.Select(attrs={"class": "normalize"}),
            "notification_criteria": forms.Select(attrs={"class": "normalize"}),
        }
