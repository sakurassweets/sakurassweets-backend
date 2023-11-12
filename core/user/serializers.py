from rest_framework import serializers
from user.models import User

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)
from components.user.utils import update_last_login


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(self.user)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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

    class Meta:
        model = User
        fields = ['email', 'password']
