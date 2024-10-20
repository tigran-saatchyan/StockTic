"""This module defines tasks for fetching tickers from an external API.

Tasks:
    fetch_tickers_from_api: A Celery task to fetch tickers from an external
        API and update the database.
"""

import logging

import requests
from celery import shared_task
from django.conf import settings

from .models import Ticker

logger = logging.getLogger(__name__)


@shared_task
def fetch_tickers_from_api():
    """A Celery task to fetch tickers from an external API and update
    the database.
    """
    url = (
        f"{settings.TICKER_FETCHING_API_URL}"
        f"?apikey={settings.TICKER_FETCHING_API_KEY}"
    )
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for item in data:
            try:
                Ticker.create_or_update_from_api(item)
            except Exception as e:
                logger.error(f"Error updating ticker: {e}")
    else:
        logger.error("Failed to fetch data from external API")
