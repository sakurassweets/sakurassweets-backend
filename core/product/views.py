from rest_framework import viewsets, filters
from django_filters.rest_framework.backends import DjangoFilterBackend

from components.general.logging.backend_decorators import log_db_query
from components.product import permissions as custom_permissions
from components.general.caching.cache import cache_method

from product.models import Product, ProductType, PriceCurrency
from product import serializers


class PriceCurrencyViewset(viewsets.ModelViewSet):
    queryset = PriceCurrency.objects.all()
    serializer_class = serializers.PriceCurrencySerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]

    @cache_method(cache_key='price_currency_retrieve', timeout=60 * 60 * 12)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_method(cache_key='price_currency_list', timeout=60 * 60 * 12)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_db_query
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @log_db_query
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_db_query
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ProductTypeViewset(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]

    @cache_method(cache_key='product_type_retrieve', timeout=60 * 60 * 12)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_method(cache_key='product_type_list', timeout=60 * 60 * 12)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_db_query
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @log_db_query
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_db_query
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]
    # Cache
    cache_key = "product"
    timeout = 25
    # Filters
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
    filterset_fields = ["product_type", "price_currency", "price",
                        "quantity_in_stock", "rating", "price_currency_symbol"]
    search_fields = ["title", "description", "components"]
    ordering_fields = ["id", "price", "quantity_in_stock",
                       "rating", "discount", "title"]
    ordering = ["-id"]

    @cache_method(cache_key='product_retrieve', timeout=25)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_method(cache_key='product_list', timeout=25)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_db_query
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @log_db_query
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_db_query
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
