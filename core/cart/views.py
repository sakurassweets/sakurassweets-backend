from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from components.cart.validators import (
    CreateCartItemValidator,
    CreateCartValidator,
    UpdateCartItemValidator
)
from components.general.logging.backend_decorators import log_db_query
from components.general.caching.cache import cache_method
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

    @cache_method(cache_key="cart_list", timeout=60 * 2)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_method(cache_key="cart_retrieve", timeout=60 * 2)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @log_db_query
    def create(self, request: Request, *args, **kwargs) -> Response:
        validator = CreateCartValidator(request)
        _perform_validation(validator)

        return super().create(request, *args, **kwargs)

    @log_db_query
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_db_query
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


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

    @cache_method(cache_key="cart_item_list", timeout=60 * 2)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_method(cache_key="cart_item_retrieve", timeout=60 * 2)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @log_db_query
    def create(self, request: Request, *args, **kwargs) -> Response:
        validator = CreateCartItemValidator(request)
        _perform_validation(validator)

        return super().create(request, *args, **kwargs)

    @log_db_query
    def partial_update(self, request, *args, **kwargs):
        validator = UpdateCartItemValidator(request)
        _perform_validation(validator)

        return super().partial_update(request, *args, **kwargs)

    @log_db_query
    def update(self, request, *args, **kwargs):

        validator = UpdateCartItemValidator(request)
        _perform_validation(validator)

        return super().update(request, *args, **kwargs)
