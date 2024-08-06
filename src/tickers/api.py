from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tickers.models import Ticker
from tickers.serializers import TickerSerializer


class TickerViewSet(viewsets.ModelViewSet):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    @action(detail=False, methods=['get'])
    def get_by_symbol(self, request):
        symbol = request.query_params.get('symbol', None)
        if symbol is not None:
            ticker = self.queryset.filter(symbol=symbol).first()
            if ticker:
                serializer = self.get_serializer(ticker)
                return Response(serializer.data)
        return Response({"detail": "Not found."}, status=404)
