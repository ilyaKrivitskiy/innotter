from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PageSerializer, TagSerializer, PostSerializer
from .models import Page, Tag, Post
from rest_framework.response import Response


class PageViewSet(viewsets.ViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class TagViewSet(viewsets.ViewSet):
    serializer_class = PageSerializer
    queryset = Tag.objects.all()


class PostViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    queryset = Tag.objects.all()
