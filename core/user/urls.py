from django.urls import path
from user import views

urlpatterns = [
    path('', views.Test.as_view(), name='test')
]
