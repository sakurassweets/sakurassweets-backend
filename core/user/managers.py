from django.utils.translation import gettext as _
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from components.user.validators import UserValidator
from user.serializers import CreateUserSerializer
from user.models import User


class UserCreateManager:
    """
    Manager that provide user creation.

    Provides validation and other things behind the scene
    """
    @classmethod
    def create_user(cls, serializer: CreateUserSerializer) -> dict:
        """
        Method to create user account

        Input:
        - serializer - can be a serializer that targets only user creation
        """
        email, password = cls._get_user_data(serializer)
        user = cls._create_user(password, email)
        cls._set_user_properties(password, user)
        return cls._build_context(user)

    @staticmethod
    def _get_user_data(serializer: CreateUserSerializer) -> tuple[str, str]:
        """
        Returns tuple with email and password after serializing it
        """
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        return email, password

    @staticmethod
    def _create_user(password: str, email: str) -> User:
        """
        Create user after some validation

        Input:
        - password
        - email

        Output:
        - created User model instance
        """
        UserValidator.validate(password, email)
        return User.objects.create_user(password=password, email=email)

    @staticmethod
    def _build_context(user: User) -> dict:
        """
        Gets tokens for created user and sends it as response

        Input:
        - User model instance

        Output:
        - context dictionary
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

        Input:
        - password
        - User instance
        """
        user.set_password(password)
        user.last_login = timezone.now()
        user.save()


class UserDeleteManager:
    _error_message = _("Something went wrong during user delition")
    _permission_error_message = _("You have no permission to delete this user")

    def delete(self, request, pk: int) -> Response:
        user = request.user

        if not self._check_permission(user, pk):
            return Response({"errors": self._permission_error_message})

        self._delete_user(pk)
        if self._check_user_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"errors": self._error_message})

    def _delete_user(self, pk: int) -> None:
        user = User.objects.get(id=pk)
        user.delete()

    def _check_permission(self, user, pk: str) -> bool:
        if user.id == id or user.is_superuser:
            return True

        return False

    def _check_user_deleted(self, pk) -> bool:
        try:
            User.objects.get(id=pk)
            return False
        except User.DoesNotExist:
            return True
