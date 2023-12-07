from rest_framework import viewsets, permissions

from product.models import Product
from product import serializers


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny,]
