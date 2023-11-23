from django.http import HttpRequest

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from components.user.mixins import UpdateRetrieveDestroyListUserMixin

from user.managers import (
    UserCreateManager,
    UserDeleteManager,
    UserUpdateManager
)
from user.models import User
from user.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    PartialUpdateUserSerializer
)


class UserViewSet(UpdateRetrieveDestroyListUserMixin,
                  viewsets.GenericViewSet):
    # TODO: Logg user updating/creating/deleting operations
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self) -> Serializer:
        if self.action == 'update':
            return UpdateUserSerializer
        elif self.action == 'partial_update':
            return PartialUpdateUserSerializer
        else:
            return self.serializer_class

    def retrieve(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Endpoint to retrieve user

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`
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

        **Has permissions:** Anyone
        """
        serializer = self.get_serializer_class()
        manager = UserUpdateManager()
        response = manager.update(request, serializer, pk)
        return response

    def partial_update(self, request: HttpRequest, pk: int) -> Response:
        """
        Endpoint to update user

        PATCH method required **ATLEAST ONE** field to get successful update

        **Input:** Atleast one field

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`

        **Has permissions:** Anyone
        """
        serializer = self.get_serializer_class()
        manager = UserUpdateManager()
        response = manager.partial_update(request, serializer, pk)
        return response

    def destroy(self, request: HttpRequest, pk: int) -> Response:
        """
        Endpoint to delete user

        **Input:** `id`

        **Output:** Nothing

        **Code:** `204`

        **Has permissions:** Anyone
        """
        manager = UserDeleteManager()
        response = manager.delete(request, pk)
        return response

    def list(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Endpoint to list users

        **Output:** Users list with fields: `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`, `is_active`

        **Code:** `200`

        **Has permissions:** Anyone
        """
        return super().list(request, *args, **kwargs)


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
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
