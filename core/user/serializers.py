from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)
from rest_framework import serializers

from components.user import utils
from user.models import User


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom TokenRefreshSerializer provides a `last login` updating
    when refreshing token
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        utils.update_last_login(self.user)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer provides a `last login` updating
    when getting new token
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        utils.update_last_login(self.user)
        return data


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions for admins, except `create`,
    related to User model

    Admins have permission to extended list of fields
    """
    user_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail')

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'password']


class ListUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions, except `create`,
    related to User model
    """
    user_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail')

    class Meta:
        model = User
        fields = ['id', 'user_url', 'email',
                  'last_login', 'is_staff', 'is_active']


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `create` action for User model
    """
    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `update` action for User model
    """
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_active']


class PartialUpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `partial_update` action for User model
    """
    class Meta:
        model = User
        fields = ['is_staff', 'is_active']
