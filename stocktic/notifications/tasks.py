import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from notifications.models import Notification
from telegram_bot.utils import send_telegram_message
from tickers.services import Finance

logger = logging.getLogger(__name__)


@shared_task
def check_ticker_prices():
    notifications = Notification.objects.all()
    for notification in notifications:
        ticker = notification.ticker.symbol
        finance = Finance(ticker)
        current_price = finance.get_latest_price()

        if current_price is None:
            logger.error(f"Could not fetch price for {ticker}")
            continue

        if (
            notification.notification_criteria == "more_than"
            and current_price > notification.notification_value
        ) or (
            notification.notification_criteria == "less_than"
            and current_price < notification.notification_value
        ):
            send_notification(notification, current_price)


def send_notification(notification, current_price):
    user = notification.user
    message = (
        f"📊 The price of {notification.ticker.symbol} is now {current_price:.2f} "
        f"({notification.notification_criteria.replace('_', ' ')} {notification.notification_value:.2f})! 📈"
    )
    if notification.notification_type in ["email", "all"]:
        send_mail(
            "Price Alert",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    if notification.notification_type in ["telegram", "all"]:
        send_telegram_message(user.telegram_user_id, message)

    notification.last_notification = timezone.now()
    notification.save()
