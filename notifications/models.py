from django.db import models

from custom_utils.common.constants import NULLABLE


class Notification(models.Model):
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
        return self.ticker
