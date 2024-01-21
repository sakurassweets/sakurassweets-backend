"""Collects all routes into one router.

Router include all endpoints that are will be displayed on API root.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import UserViewSet, CreateUserViewSet
from image.views import ImageViewSet
from product.views import (
    ProductViewset,
    PriceCurrencyViewset,
    ProductTypeViewset
)
from cart.views import CartViewSet, CartItemViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', CreateUserViewSet, basename='user-register')
router.register(r'products', ProductViewset, basename='product')
router.register(r'product-types', ProductTypeViewset, basename='product-type')
router.register(r'price-currencies', PriceCurrencyViewset,
                basename='price-currency')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    # JWT token endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
