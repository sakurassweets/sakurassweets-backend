from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import UserViewSet, CreateUserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', CreateUserViewSet, basename='user-register')

urlpatterns = [
    path('', include(router.urls)),
    # JWT token endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
