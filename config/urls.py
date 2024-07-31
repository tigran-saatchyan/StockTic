from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

django_urlpatterns = [
    path("admin/", admin.site.urls),

]

app_urlpatterns = [
    path('', include('dashboard.urls')),
    path('stocks/', include('stocks.urls')),
    path('watchlist/', include('watchlist.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('historical-data/', include('historical_data.urls')),
    path('tickers/', include('tickers.urls')),
    path('finance-reports/', include('finance_reports.urls')),
]

third_party_urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include('django_prometheus.urls')),
]

urlpatterns = django_urlpatterns + app_urlpatterns + third_party_urlpatterns
