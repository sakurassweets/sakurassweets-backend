from rest_framework import permissions
from cart.models import Cart


class IsCartOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        cart = Cart.objects.get(id=obj.cart_id)

        if request.user.id == cart.cart_owner.id:
            return True

        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
