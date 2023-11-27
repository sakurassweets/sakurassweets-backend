from typing import Literal

from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _
from django.http import HttpRequest
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status

from components.user.validators import UserValidator
from components.user import constants
from user.models import User


class UserCreateManager:
    """
    Manager that provide user creation.

    Provides validation and other things behind the scene
    """
    @classmethod
    def create_user(cls, serializer: Serializer) -> dict:
        email, password = cls._get_user_data(serializer)
        user = cls._create_user(password, email)
        cls._set_user_properties(password, user)
        return cls._build_context(user)

    @staticmethod
    def _get_user_data(serializer: Serializer) -> tuple[str, str]:
        """
        Returns tuple with email and password after serializing it
        """
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        return email, password

    @staticmethod
    def _create_user(password: str, email: str) -> User:
        UserValidator.validate(password, email)
        return User.objects.create_user(password=password, email=email)

    @staticmethod
    def _build_context(user: User) -> dict:
        """
        Gets tokens for created user and sends it as response
        """
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        context = {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }
        return context

    @staticmethod
    def _set_user_properties(password: str, user: User) -> None:
        """
        Setting up the hashed password for user and updating last login time
        """
        password = make_password(password)
        User.objects.filter(id=user.id).update(
            last_login=timezone.now(),
            password=password
        )


class UserUpdateManager:

    _no_permission_error: str = _("You have no permission to update this user")
    _new_password_error: str = _("New password can't be the same as old one.")
    _empty_field_error: str = _("This field can't be empty.")
    _required_fields = constants.REQUIRED_UPDATE_FIELDS
    _required_field_error: str = _("This field is required")
    _updated_data: dict = {}

    def partial_update(self, request: HttpRequest, serializer: Serializer, pk: int) -> Response:
        response = self._update_and_return_response(
            request=request,
            serializer=serializer,
            pk=pk,
            partial=True
        )
        return response

    def update(self, request: HttpRequest, serializer: Serializer, pk: int) -> Response:
        response = self._update_and_return_response(request, serializer, pk)
        return response

    def _update_and_return_response(self,
                                    request: HttpRequest,
                                    serializer: Serializer,
                                    pk: int,
                                    partial: bool = False) -> Response:
        request_user = request.user
        data = request.data

        if not partial:
            response_required = self._validate_required_fields(data)
            if response_required is not None:
                return Response({"detail": response_required},
                                status=status.HTTP_400_BAD_REQUEST)

        response_empty = self._validate_empty_fields(data)
        if response_empty is not None:
            return Response({"detail": response_empty},
                            status=status.HTTP_400_BAD_REQUEST)

        data, status_ = self._update_user(request_user, data, serializer, pk)
        if 'detail' in data:
            return Response(data, status_)
        return Response({"data": data}, status_)

    def perform_update(self, user: User, data: dict) -> None:
        """
        For every field in data.items() sets new value if it updated.

        save() method wouldn't be called if at least one field wouldn't be updated.
        """
        for key, value in data.items():
            if key == 'password':
                continue
            if value != getattr(user, key):
                setattr(user, key, value)
                self._updated_data[key] = value

        if len(self._updated_data.items()) > 0:
            user.save()

    def _update_user(self,
                     request_user: User,
                     data: dict,
                     serializer: Serializer,
                     pk: int) -> tuple[dict[str, str], Literal[200, 400]]:
        user = User.objects.get(id=pk)
        response = self._check_permission(request_user, user)
        if isinstance(response, tuple):
            response, status_ = response
            return response, status_

        validated_data_response = self._validate_data(user, data, serializer)
        if isinstance(validated_data_response, tuple):
            message, status_ = validated_data_response
            if message:
                return message, status_

        # if we get new password we change only password and doesn't care about other fields
        if 'new_password' in data:
            new_password = data.get('new_password')
            response, status_ = self._change_password(user, new_password)
            return response, status_
        else:
            self.perform_update(user, data)

        return self._updated_data, status.HTTP_200_OK

    def _validate_empty_fields(self, data: dict) -> dict | None:
        errors: dict = {}
        for key, value in data.items():
            if not value:
                errors[key] = self._empty_field_error

        return errors if errors else None

    def _validate_required_fields(self, data: dict) -> dict | None:
        errors: dict = {}
        for field in self._required_fields:
            if field not in data:
                errors[field] = self._required_field_error

        return errors if errors else None

    def _check_permission(self,
                          request_user: User,
                          user: User) -> tuple[dict[str, str], Literal[400]] | Literal[False]:
        if request_user.id == user.id or request_user.is_superuser:
            return False
        else:
            return {"detail": self._no_permission_error}, status.HTTP_400_BAD_REQUEST

    def _change_password(self, user: User, new_password: str) -> tuple[dict[str, str], Literal[200, 400]]:
        response = self._validate_new_password(
            new_password=new_password,
            user=user
        )
        if response is None:
            user.password = new_password
            user.save()
            self._updated_data['new_password'] = user.password
            return self._updated_data, status.HTTP_200_OK
        else:
            return {"detail": response}, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def _validate_data(user: User,
                       data: dict,
                       serializer: Serializer) -> tuple[dict[str, str], Literal[400]] | Literal[False]:
        user_email = user.email
        request_email = data.get('email')
        try:
            serializer = serializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            # avoid error raised by unique values
            if user_email == request_email:
                return False
            else:
                return {"detail": error}, status.HTTP_400_BAD_REQUEST

    def _validate_new_password(self, user: User, new_password: str) -> dict | None:
        """
        Validate new password

        Output:
        - dict - If some errors occured they returned as dictionary
        - None - returns None if everything okay and errors didn't occur.
        """
        check_password = user.check_password(new_password)
        if check_password:
            # returns this if new password is the same as old one
            return {"new_password": self._new_password_error}

        return None


class UserDeleteManager:
    _error_message = _("Something went wrong during user delition")
    _permission_error_message = _("You have no permission to delete this user")

    def delete(self, request: HttpRequest, pk: int) -> Response:
        user = request.user

        if not self._check_permission(user, pk):
            return Response({"detail": self._permission_error_message})

        self._delete_user(pk)
        if self._check_user_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": self._error_message})

    def _delete_user(self, pk: int) -> None:
        user = User.objects.get(id=pk)
        user.delete()

    def _check_permission(self, user: User, pk: str) -> bool:
        if user.id == pk or user.is_superuser:
            return True

        return False

    @staticmethod
    def _check_user_deleted(pk: int) -> bool:
        try:
            User.objects.get(id=pk)
            return False
        except User.DoesNotExist:
            return True
