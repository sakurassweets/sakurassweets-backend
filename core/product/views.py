from rest_framework import viewsets

from components.product.caching.caching_decorators import cache_product_method
from components.product import permissions as custom_permissions

from product.models import Product, ProductType, PriceCurrency
from product import serializers


class PriceCurrencyViewset(viewsets.ModelViewSet):
    queryset = PriceCurrency.objects.all()
    serializer_class = serializers.PriceCurrencySerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]

    @cache_product_method(cache_key='price_currency_retrieve', timeout=60 * 60 * 12)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_product_method(cache_key='price_currency_list', timeout=60 * 60 * 12)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductTypeViewset(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]

    @cache_product_method(cache_key='product_type_retrieve', timeout=60 * 60 * 12)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_product_method(cache_key='product_type_list', timeout=60 * 60 * 12)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]

    @cache_product_method(cache_key='product_retrieve', timeout=60 * 60 * 12)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_product_method(cache_key='product_list', timeout=60 * 60 * 12)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
