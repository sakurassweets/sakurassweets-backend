from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from components.cart.validators import CreateCartItemValidator, CreateCartValidator, UpdateCartItemValidator
from components.cart import permissions as cart_permissions
from components.cart_item import permissions as cart_item_permissions
from cart import constants


def _perform_validation(validator):
    result = validator.validate()
    if isinstance(result, (str, dict)):
        raise ValidationError({"detail": result})

    return True


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action in constants.SAFE_ACTIONS:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in constants.PRIVATE_ACTIONS:
            return [cart_permissions.IsCartOwnerOrStaff()]
        else:
            return []

    def create(self, request: Request, *args, **kwargs) -> Response:
        validator = CreateCartValidator(request)
        _perform_validation(validator)

        return super().create(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action in constants.SAFE_ACTIONS:
            return [permissions.AllowAny()]
        elif self.action in constants.PRIVATE_ACTIONS or self.action == 'create':
            return [cart_item_permissions.IsCartOwnerOrStaff()]
        else:
            return []

    def create(self, request: Request, *args, **kwargs) -> Response:
        validator = CreateCartItemValidator(request)
        _perform_validation(validator)

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        validator = UpdateCartItemValidator(request)
        _perform_validation(validator)

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        validator = UpdateCartItemValidator(request)
        _perform_validation(validator)

        return super().update(request, *args, **kwargs)
