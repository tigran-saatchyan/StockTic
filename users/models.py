from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from custom_utils.common.constants import NULLABLE
from custom_utils.utils import save_picture
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="email",
        validators=[validators.EmailValidator(message="Invalid Email")],
    )
    telephone = models.CharField(max_length=50, verbose_name="telephone", **NULLABLE)
    image = models.ImageField(upload_to=save_picture, verbose_name="avatar", **NULLABLE)
    telegram_user_id = models.IntegerField(**NULLABLE, verbose_name="telegram user id")
    is_verified: bool = models.BooleanField(verbose_name="is verified", default=False)
    is_active = models.BooleanField(
        verbose_name="is active",
        default=False,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_modified: datetime = models.DateTimeField(
        verbose_name="date modified", auto_now=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            str: The user's full name and email address.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("date_joined",)
