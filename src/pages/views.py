from django.shortcuts import render
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from users import permissions
from users.authentication import JWTAuthentication
from users.permissions import IsNotBlocked
from .serializers import PageSerializer, TagSerializer, PostSerializer
from .models import Page, Tag, Post
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.request import Request


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    authentication_classes = [JWTAuthentication]

    permission_classes_by_action = {
        'list': [permissions.IsStaffUser],
        'retrieve': [permissions.IsOwnPageOrStaffUser],
        'create': [IsAuthenticated],
        'update': [permissions.IsOwnPageOrReadOnly],
        'partial_update': [permissions.IsOwnPageOrReadOnly],
        'destroy': [permissions.IsOwnPageOrReadOnly],
        'change_block': [permissions.IsStaffUser],
        'change_block_permanent': [permissions.IsAdminRole],
        'change_access': [permissions.IsOwnPageOrReadOnly],
        'follow': [IsNotBlocked],
        'list_follow_requests': [permissions.IsOwnPageOrReadOnly],
        'accept_follow_requests': [permissions.IsOwnPageOrReadOnly],
        'accept_follow_request': [permissions.IsOwnPageOrReadOnly]
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def follow(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        user = request.user
        if user == page.owner:
            return Response(data="You cant follow yourself!", status=status.HTTP_403_FORBIDDEN)
        if user in page.followers.all() or user in page.follow_requests.all():
            return Response(data="You already following this page!", status=status.HTTP_403_FORBIDDEN)
        if page.is_private:
            page.follow_requests.add(user)
            page.save()
            return Response("Your request had send!")
        page.followers.add(user)
        page.save()
        return Response("You are following this page now!")

    @action(detail=True, methods=['get'])
    def list_follow_requests(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        if not page.is_private:
            return Response(data="You have no follow requests (your page is not private).")
        serializer = self.serializer_class(page, partial=True)
        return Response(data={"follow_requests": serializer.data["follow_requests"]})

    @action(detail=True, methods=['patch'])
    def accept_follow_requests(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        if not page.is_private:
            return Response(data="You have no follow requests (your page is not private).")
        serializer = self.serializer_class(page, partial=True)
        page.followers.set(page.followers.all() | page.follow_requests.all())
        page.follow_requests.set([])
        return Response(data=serializer.data)

    @action(detail=True, methods=['patch'], url_path="accept_follow_request/(?P<follower_id>[^/.]+)")
    def accept_follow_request(self, request: Request, pk=None, follower_id=None):
        page = get_object_or_404(Page, pk=pk)
        if not page.is_private:
            return Response(data="You have no follow requests (your page is not private).")
        serializer = self.serializer_class(page, partial=True)
        page.followers.add(page.follow_requests.get(pk=follower_id))
        page.follow_requests.remove(follower_id)
        return Response(data=serializer.data)

    @action(detail=True, methods=['patch'])
    def change_access(self, request: Request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        page.is_private = False if page.is_private else True
        page.save(update_fields=["is_private"])
        return Response({"is_private": page.is_private})

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
    authentication_classes = [JWTAuthentication]
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
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]

    permission_classes_by_action = {
        'create': [permissions.IsNotBlocked],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [permissions.IsOwnPostOrReadOnly],
        'partial_update': [permissions.IsOwnPostOrReadOnly],
        'destroy': [permissions.IsOwnPostOrStaffUser],
        'like': [permissions.IsOwnerOrStaffUser, IsNotBlocked],
        'reply': [IsNotBlocked]
    }

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(post, partial=True)
        user = request.user
        if user not in post.likes.all():
            post.likes.add(user)
        else:
            post.likes.remove(user.id)
        post.save()
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def reply(self, request: Request, pk=None):
        serializer = self.serializer_class(Post(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(reply_to=get_object_or_404(Post, pk=pk))
        return Response(data=serializer.data)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
