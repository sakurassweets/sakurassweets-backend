from rest_framework import permissions


class IsCartOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.id == obj.cart_owner.id:
            return True

        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
