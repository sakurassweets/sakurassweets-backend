from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)
from rest_framework import serializers

from components.user import utils
from user.models import User


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """Provides a `last login` updatingwhen refreshing token."""

    def validate(self, attrs):
        data = super().validate(attrs)
        utils.update_last_login(self.user)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Provides a `last login` updating when getting new token."""

    def validate(self, attrs):
        data = super().validate(attrs)
        utils.update_last_login(self.user)
        return data


class AdminUserSerializer(serializers.ModelSerializer):
    """Provides all actions for admins, except `create` for `User` model.

    Admins have permission to extended list of fields
    """
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')  # NOQA

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'password']


class ListUserSerializer(serializers.ModelSerializer):
    """Provides all actions, except `create` for `User` model."""
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')  # NOQA

    class Meta:
        model = User
        fields = ['id', 'user_url', 'email',
                  'last_login', 'is_staff', 'is_active']


class CreateUserSerializer(serializers.ModelSerializer):
    """Provides `create` action for `User` model."""
    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateUserSerializer(serializers.ModelSerializer):
    """Provides `update` action for `User` model."""
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_active']


class PartialUpdateUserSerializer(serializers.ModelSerializer):
    """Provides `partial_update` action for `User` model."""
    class Meta:
        model = User
        fields = ['is_staff', 'is_active']
