from rest_framework import viewsets

from components.product import permissions as custom_permissions

from product.models import Product, ProductType, PriceCurrency
from product import serializers


class PriceCurrencyViewset(viewsets.ModelViewSet):
    queryset = PriceCurrency.objects.all()
    serializer_class = serializers.PriceCurrencySerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]


class ProductTypeViewset(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [custom_permissions.IsAdminOrStaff,]
