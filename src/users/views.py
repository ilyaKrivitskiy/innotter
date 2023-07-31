from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoObjectPermissions
from .serializers import UserSerializer, UserSignUpSerializer
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.request import Request
from rest_framework.response import Response
from .permissions import IsSuperUser, IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    serializer_classes_by_action = {
        'create': UserSignUpSerializer
    }
    default_serializer_class = UserSerializer

    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [AllowAny],
        'update': [IsOwnerOrReadOnly],
        'partial_update': [IsOwnerOrReadOnly],
        'destroy': [IsSuperUser]
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
