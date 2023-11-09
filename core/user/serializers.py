from rest_framework import serializers
from user.models import User


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
