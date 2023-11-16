from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import CreateUserSerializer
from user.models import User


class UserCreateManager:
    # TODO: add more validation methods
    @classmethod
    def create_user(cls, serializer: CreateUserSerializer) -> dict:
        """
        Method to create user account

        This method performs password hashing and updating last login time
        """
        email, password = cls._get_user_data(serializer)
        user = cls._create_user(email, password)
        cls._set_user_properties(user, password)
        return cls._build_context(user)

    @staticmethod
    def _get_user_data(serializer: CreateUserSerializer) -> tuple:
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['email'], serializer.validated_data['password']

    @staticmethod
    def _create_user(email: str, password: str) -> User:
        return User.objects.create_user(email=email, password=password)

    @staticmethod
    def _build_context(user: User) -> dict:
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }

    @staticmethod
    def _set_user_properties(user: User, password: str) -> None:
        user.set_password(password)
        user.last_login = timezone.now()
        user.save()
