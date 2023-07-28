from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .serializers import PageSerializer, TagSerializer, PostSerializer
from .models import Page, Tag, Post
from rest_framework import mixins
from rest_framework.response import Response


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Tag.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Tag.objects.all()
