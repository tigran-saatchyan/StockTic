import requests
from django.conf import settings
from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tickers.models import Ticker
from tickers.serializers import TickerSerializer


class TickerViewSet(viewsets.ModelViewSet):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    @action(detail=False, methods=["get"])
    def get_by_symbol(self, request):
        symbol = request.query_params.get("symbol", None)
        if symbol is not None:
            ticker = self.queryset.filter(symbol=symbol).first()
            if ticker:
                serializer = self.get_serializer(ticker)
                return Response(serializer.data)
        return Response({"detail": "Not found."}, status=404)


class FetchTickersAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        url = f"{settings.TICKER_FETCHING_API_URL}?apikey={settings.TICKER_FETCHING_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for item in data:
                try:
                    Ticker.create_or_update_from_api(item)
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {"message": "Tickers fetched and saved/updated successfully!"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Failed to fetch data from external API"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
