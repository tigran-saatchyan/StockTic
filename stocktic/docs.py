"""This module configures the API documentation views for the StockTic project
using drf_yasg and Django REST framework.

It sets up the schema view for Swagger and ReDoc UI, and defines
the URL patterns for accessing these documentation interfaces.
"""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="StockTic API",
        default_version="v1",
        description="API for StockTic",
        # terms_of_service="https://github.com/tigran-saatchyan"
        #                  "/StockTic/blob/"
        #                  "develop/TERMS_OF_SERVICE",
        contact=openapi.Contact(
            email="mr.saatchyan@gmail.com",
            name="Tigran Saatchyan",
            url="https://github.com/tigran-saatchyan",
        ),
        license=openapi.License(
            name="MIT License",
            # url="https://github.com/tigran-saatchyan/"
            #     "StockTic/blob/develop/LICENSE"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
