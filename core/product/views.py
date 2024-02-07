from rest_framework import filters
from django_filters.rest_framework.backends import DjangoFilterBackend

from components.product import permissions as custom_permissions

from product.models import Product, ProductType, PriceCurrency
from components.general.caching.viewsets import CacheModelViewSet
from product import serializers


class PriceCurrencyViewset(CacheModelViewSet):
    queryset = PriceCurrency.objects.all()
    cache_key = "price_currency"
    timeout = 60 * 60 * 12
    serializer_class = serializers.PriceCurrencySerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]


class ProductTypeViewset(CacheModelViewSet):
    queryset = ProductType.objects.all()
    cache_key = "product_type"
    timeout = 60 * 60 * 12
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]


class ProductViewset(CacheModelViewSet):
    queryset = Product.objects.all()
    cache_key = "product"
    timeout = 25
    serializer_class = serializers.ProductSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]
    # Filters
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        "product_type", "price_currency", "price", "quantity_in_stock", "rating"
    ]
    search_fields = [
        "title", "description", "components"
    ]
    ordering_fields = [
        "id", "price", "quantity_in_stock", "rating", "discount", "title"
    ]
    ordering = ["-id"]
