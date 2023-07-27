from django.urls import path, include
from rest_framework import routers
from .views import PageViewSet, TagViewSet, PostViewSet

page_router = routers.DefaultRouter(trailing_slash=False)
page_router.register('pages', PageViewSet, basename="pages")
page_router.register('tags', TagViewSet, basename="tags")
page_router.register('posts', PostViewSet, basename="posts")

urlpatterns = [
    path('', include(page_router.urls))
]
