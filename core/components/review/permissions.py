from rest_framework import permissions


class IsReviewOwnerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return request.user.is_authenticated
        return request.user.is_staff or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.user:
            return True
        return request.user.is_staff or request.user.is_superuser
