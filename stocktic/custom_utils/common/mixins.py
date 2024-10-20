"""This module provides mixins for common model fields and form styling in
the Django project.

Mixins:
    DateFieldsMixin: Adds date_created and date_modified fields to a model.
    FormStyleMixin: Adds a CSS class to form fields for consistent styling.
"""

from django.db import models


class DateFieldsMixin(models.Model):
    """A mixin that adds date_created and date_modified fields to a model.

    Attributes:
        date_created (DateTimeField): The date and time when the object
            was created.
        date_modified (DateTimeField): The date and time when the object
            was last modified.
    """

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created",
        help_text="Date Created",
    )
    date_modified = models.DateTimeField(
        auto_now=True, verbose_name="Date Modified", help_text="Date Modified"
    )

    class Meta:
        abstract = True


class FormStyleMixin:
    """A mixin that adds a CSS class to form fields for consistent styling.

    Methods:
        __init__: Initializes the mixin and adds the CSS class to form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
