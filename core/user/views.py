from django.http import HttpRequest

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from components.user.mixins import UpdateRetrieveDestroyListUserMixin
from components.user.caching.caching_decorators import cache_user_method

from user.managers import (
    UserCreateManager,
    UserDeleteManager,
    UserUpdateManager
)
from user.models import User
from user import serializers


class UserViewSet(UpdateRetrieveDestroyListUserMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ListUserSerializer
    permission_classes = [permissions.AllowAny]
    serializers_map = {
        'update': serializers.UpdateUserSerializer,
        'partial_update': serializers.PartialUpdateUserSerializer,
        'list': serializers.ListUserSerializer
    }

    def get_serializer_class(self) -> Serializer:
        if self.action in ['list', 'retrieve'] and self.request.user.is_staff:
            return serializers.AdminUserSerializer

        if self.action in self.serializers_map:
            return self.serializers_map[self.action]
        else:
            return self.serializer_class

    @cache_user_method(cache_key='user_retrieve', timeout=60 * 60)
    def retrieve(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Endpoint to retrieve user

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`

        **Has permissions:** Anyone
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request: HttpRequest, pk: int) -> Response:
        """
        Endpoint to update user

        PUT method required **ALL** fields to get successful update

        **Input:** `email`, `password` (raw)

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`

        **Has permissions:** User itself or admin
        """
        return self._handle_update(request, pk, partial=False)

    def partial_update(self, request: HttpRequest, pk: int) -> Response:
        """
        Endpoint to update user

        PATCH method required **ATLEAST ONE** field to get successful update

        **Input:** Atleast one field

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`

        **Has permissions:** User itself or admin
        """
        return self._handle_update(request, pk, partial=True)

    def destroy(self, request: HttpRequest, pk: int) -> Response:
        """
        Endpoint to delete user

        **Input:** `id`

        **Output:** Nothing

        **Code:** `204`

        **Has permissions:** User itself or admin
        """
        manager = UserDeleteManager()
        response = manager.delete(request=request, pk=pk)
        return response

    @cache_user_method(cache_key='user_list', timeout=60 * 60)
    def list(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Endpoint to list users

        **Output:** Users list with fields: `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`, `is_active`

        **Code:** `200`

        **Has permissions:** Anyone
        """
        return super().list(request, *args, **kwargs)

    def _handle_update(self, request: HttpRequest, pk: int, partial: bool) -> Response:
        """
        Common method to handle both full and partial updates.
        """
        serializer = self.get_serializer_class()
        manager = UserUpdateManager()

        if partial:
            response = manager.partial_update(
                request=request,
                serializer=serializer,
                pk=pk
            )
        else:
            response = manager.update(
                request=request,
                serializer=serializer,
                pk=pk
            )

        return response


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.AllowAny,]

    def create(self, request: HttpRequest) -> Response:
        """
        User register endpoint

        **Input:** `Email`, `Password`

        **Output:** `Access token`, `Refresh token`

        **Permissions:** Anyone
        """
        serializer = self.get_serializer(data=request.data)

        context = UserCreateManager.create_user(serializer)
        return Response(context, status=status.HTTP_201_CREATED)
