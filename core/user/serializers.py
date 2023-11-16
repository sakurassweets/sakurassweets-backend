from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)
from rest_framework import serializers

from components.user.utils import update_last_login
from user.models import User


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom TokenRefreshSerializer provides a `last login` updating
    when refreshing token
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(self.user)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer provides a `last login` updating
    when getting new token
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions, except `create`,
    related to User model
    """
    user_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail')

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'password']


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `create` action for User model
    """
    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `update` and `partial_update` actions
    for User model
    """
    class Meta:
        model = User
        fields = ['email', 'password', 'is_staff', 'is_active']
