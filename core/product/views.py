from rest_framework import viewsets, permissions

from product.models import Product, ProductType, PriceCurrency
from product import serializers


class PriceCurrencyViewset(viewsets.ModelViewSet):
    queryset = PriceCurrency.objects.all()
    serializer_class = serializers.PriceCurrency
    permission_classes = [permissions.AllowAny,]


class ProductTypeViewset(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    permission_classes = [permissions.AllowAny,]


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny,]
