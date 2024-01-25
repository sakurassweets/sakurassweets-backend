from rest_framework.request import Request

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from components.user.mixins import UpdateRetrieveDestroyListUserMixin
from components.user.constants import CACHE_TIMEOUT
from components.general.caching.cache import cache_method

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

    @cache_method(cache_key='user_list', timeout=CACHE_TIMEOUT)
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @cache_method(cache_key='user_retrieve', timeout=CACHE_TIMEOUT)
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def update(self, request: Request, pk: int) -> Response:
        """Updates user with `PUT` method.

        Args:
            request: a DRF's `Request` object.
            pk: integer, primary key (id) of user that being updated.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
        """
        return self._handle_update(request=request, pk=pk, partial=False)

    def partial_update(self, request: Request, pk: int) -> Response:
        """Updates user with `PATCH` method.

        Args:
            request: a DRF's `Request` object.
            pk: integer, primary key (id) of user that being updated.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
        """
        return self._handle_update(request=request, pk=pk, partial=True)

    def destroy(self, request: Request, pk: int) -> Response:
        """Deletes user.

        Args:
            request: a DRF's `Request` object.
            pk: integer, primary key (id) of user that being destroyed.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 204, 400.
        """
        manager = UserDeleteManager()
        response = manager.delete(request=request, pk=pk)
        return response

    def _handle_update(self, request: Request, pk: int, partial: bool) -> Response:
        """Handles both full and partial updates.

        Args:
            request: a DRF's `Request` object.
            pk: integer, primary key (id) of user that being updated.
            partial: boolean, if True - user updating with partial_update
                method (PATCH)

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
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

    def create(self, request: Request) -> Response:
        """Creates user.

        Args:
            request: a DRF's `Request` object.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 201, 400.
        """
        serializer = self.get_serializer(data=request.data)

        context = UserCreateManager.create_user(serializer)
        return Response(context, status=status.HTTP_201_CREATED)
