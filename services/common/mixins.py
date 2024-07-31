from django.db import models
from django import forms


class DateFieldsMixin(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date Created", help_text="Date Created"
    )
    date_modified = models.DateTimeField(
        auto_now=True, verbose_name="Date Modified", help_text="Date Modified"
    )
    # Add other common fields here

    class Meta:
        abstract = True


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
