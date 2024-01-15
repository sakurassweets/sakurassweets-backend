from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.http.request import HttpRequest

from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from components.cart.validators import CartItemValidator, CartValidator
from cart import constants


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action in constants.SAFE_ACTIONS:
            return [permissions.AllowAny()]
        elif self.action in constants.PRIVATE_ACTIONS:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        validator = CartValidator(request)

        result = validator.validate_cart_creation()
        if isinstance(result, str):
            raise APIException(result)

        return super().create(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action in constants.SAFE_ACTIONS:
            return [permissions.AllowAny()]
        elif self.action in constants.PRIVATE_ACTIONS:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        validator = CartItemValidator(request)

        result = validator.validate_cart_item_creation()
        if isinstance(result, str):
            raise APIException(result)

        return super().create(request, *args, **kwargs)
