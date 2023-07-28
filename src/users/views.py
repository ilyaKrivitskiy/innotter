from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, UserSignUpSerializer
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
