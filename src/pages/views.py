from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from users import permissions
from .serializers import PageSerializer, TagSerializer, PostSerializer
from .models import Page, Tag, Post
from rest_framework import mixins
from rest_framework.response import Response


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes_by_action = {
        'list': [permissions.IsStaffUser],
        'retrieve': [permissions.IsOwnerOrStuffUser],
        'create': [IsAuthenticated],
        'update': [permissions.IsOwnerOrReadOnly],
        'partial_update': [permissions.IsOwnerOrReadOnly],
        'destroy': [permissions.IsOwnerOrReadOnly]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Tag.objects.all()
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [permissions.IsOwnerOrReadOnly],
        'destroy': [permissions.IsOwnerOrReadOnly]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Tag.objects.all()

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [permissions.IsOwnerOrReadOnly],
        'partial_update': [permissions.IsOwnerOrReadOnly],
        'destroy': [permissions.IsOwnerOrStuffUser]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
