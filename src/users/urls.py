from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

user_router = routers.DefaultRouter(trailing_slash=False)
user_router.register('users', UserViewSet, basename="users")

urlpatterns = [
    path('', include(user_router.urls))
]
