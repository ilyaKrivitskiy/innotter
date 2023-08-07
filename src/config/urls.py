"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from users.urls import user_router
from pages.urls import page_router
import users
import pages
from users.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, LogoutAPIView

router = DefaultRouter(trailing_slash=False)
router.registry.extend(user_router.registry)
router.registry.extend(page_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('refresh', RefreshTokenAPIView.as_view()),
    path('logout', LogoutAPIView.as_view())
]
