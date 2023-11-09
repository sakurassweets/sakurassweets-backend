from rest_framework import viewsets, permissions, status
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Input:
            - Email
            - Password

        Output:
            - Access token
            - Refresh token
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        context = {
            'access': str(access_token),
            'refresh': str(refresh),
        }
        headers = self.get_success_headers(serializer.data)
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)
