"""This module defines the models for the notifications app.

Models:
    Notification: A model representing a notification instance.
"""

from custom_utils.common.constants import NULLABLE
from django.db import models


class Notification(models.Model):
    """A model representing a notification instance.

    Attributes:
        user (ForeignKey): The user associated with the notification.
        last_notification (DateTimeField): The date and time of the
            last notification.
        ticker (ForeignKey): The ticker associated with the notification.
        notification_value (DecimalField): The value for the notification.
        notification_type (CharField): The type of notification
            (email, telegram, all).
        notification_criteria (CharField): The criteria for the notification
            (more_than, less_than).
        date_created (DateTimeField): The date and time when the
            notification was created.
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="notifications"
    )

    last_notification = models.DateTimeField(
        **NULLABLE, verbose_name="Last notification"
    )
    ticker = models.ForeignKey(
        "tickers.Ticker",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Ticker",
    )
    notification_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Notification value",
        **NULLABLE,
    )
    notification_type = models.CharField(
        max_length=10,
        choices=[
            ("email", "Email"),
            ("telegram", "Telegram"),
            ("all", "All"),
        ],
        default="telegram",
        verbose_name="Notification type",
        **NULLABLE,
    )
    notification_criteria = models.CharField(
        max_length=10,
        choices=[
            ("more_than", "More than"),
            ("less_than", "Less than"),
        ],
        default="less_than",
        verbose_name="Notification criteria",
        **NULLABLE,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the Notification instance."""
        return self.ticker
