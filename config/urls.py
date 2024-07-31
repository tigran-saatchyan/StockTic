from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_v1 = 'api/v1/'

django_urlpatterns = [
    path("admin/", admin.site.urls),

]

app_urlpatterns = [
    path('', include('dashboard.urls')),
    path('stocks/', include('stocks.urls')),
    path('watchlist/', include('watchlist.urls')),
    path('portfolio/', include('portfolio.urls')),
    path(
        'historical-data/',
        include('historical_data.urls')
    ),
    path('tickers/', include('tickers.urls')),
    path(
        'finance-reports/',
        include('finance_reports.urls')
    ),
]

api_urlpatterns = [
    path(api_v1, include('users.urls')),
    path(api_v1, include('notifications.urls')),
    path(api_v1, include('tickers.api_urls')),
]

api_token_urlpatterns = [
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
]

third_party_urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include('django_prometheus.urls')),
]

urlpatterns = [
    *django_urlpatterns,
    *app_urlpatterns,
    *api_urlpatterns,
    *api_token_urlpatterns,
    *third_party_urlpatterns
]
