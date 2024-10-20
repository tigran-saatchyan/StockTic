import requests
from celery import shared_task
from django.conf import settings

from .models import Ticker


@shared_task
def fetch_tickers_from_api():
    url = (
        f"{settings.TICKER_FETCHING_API_URL}?apikey={settings.TICKER_FETCHING_API_KEY}"
    )
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for item in data:
            try:
                Ticker.create_or_update_from_api(item)
            except Exception as e:
                print(f"Error updating ticker: {e}")
    else:
        print("Failed to fetch data from external API")
