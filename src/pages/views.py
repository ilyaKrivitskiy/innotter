from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from users import permissions
from .serializers import PageSerializer, TagSerializer, PostSerializer
from .models import Page, Tag, Post
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.request import Request


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes_by_action = {
        'list': [permissions.IsStaffUser],
        'retrieve': [permissions.IsOwnerOrStuffUser],
        'create': [IsAuthenticated],
        'update': [permissions.IsOwnerOrReadOnly],
        'partial_update': [permissions.IsOwnerOrReadOnly],
        'destroy': [permissions.IsOwnerOrReadOnly],
        'change_block': [permissions.IsStaffUser],
        'change_block_permanent': [permissions.IsAdminRole],
        'change_access': [permissions.IsOwnerOrReadOnly]
    }

    @action(detail=True, methods=['patch'])
    def change_access(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        page.is_private = request.data["is_private"]
        page.save(update_fields=["is_private"])
        return Response(f'Private: {request.data}')

    @action(detail=True, methods=['patch'])
    def change_block(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        status = request.data["is_blocked"]
        if page.is_blocked == status:
            return Response(f"The page block status is already {page.is_blocked}")
        page.is_blocked = status
        page.unblock_date = serializer.validated_data['unblock_date']
        page.save(update_fields=["is_blocked", "unblock_date"])
        return Response("The page block status has changed!")

    @action(detail=True, methods=['patch'])
    def block_page_permanent(self, request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        status = request.data["is_blocked"]
        if page.is_blocked == status:
            return Response(f"The page block status is already {page.is_blocked}")
        page.is_blocked = status
        page.save(update_fields=["is_blocked"])
        return Response("The page block status has changed!")

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
        'create': [permissions.IsOwnerOrReadOnly],
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
