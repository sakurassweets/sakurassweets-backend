from rest_framework import viewsets, permissions, status, mixins
from django.http import HttpRequest
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer
from components.user.mixins import UpdateRetrieveDestroyListUserMixin
from user.managers import UserCreateManager


class UserViewSet(UpdateRetrieveDestroyListUserMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to retrieve user

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint to update user

        PUT method required **ALL** fields to get successful update but since we have
        only one field: `email`, it's one and only field required

        **Input:** `email`

        **Output:** `id`, `user_url`, `last_login`, `email`,
        `created_at`, `updated_at`, `is_superuser`, `is_staff`,
        `is_active`

        **Code:** `200`

        **Has permissions:** Anyone
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
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
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint to delete user

        **Input:** `id`

        **Output:** Nothing

        **Code:** `204`

        **Has permissions:** Anyone
        """
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
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

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        User register endpoint

        **Input:** `Email`, `Password`

        **Output:** `Access token`, `Refresh token`

        **Permissions:** Anyone
        """
        serializer = self.get_serializer(data=request.data)

        context = UserCreateManager.create_user(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)
