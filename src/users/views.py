import datetime
import os
import jwt
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.settings import SECRET_KEY, REFRESH_TOKEN_SECRET
from .serializers import UserSerializer, UserSignUpSerializer
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from .authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework.request import Request
from rest_framework.response import Response
from .permissions import IsSuperUser, IsOwnerOrReadOnly, IsAdminRole
from .tokens import generate_access_token, generate_refresh_token


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    serializer_classes_by_action = {
        'create': UserSignUpSerializer
    }
    default_serializer_class = UserSerializer

    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsSuperUser],
        'update': [IsOwnerOrReadOnly],
        'partial_update': [IsOwnerOrReadOnly],
        'destroy': [AllowAny],
        'block_user': [IsAdminRole],
        'register': [AllowAny],
        'login': [AllowAny],
        'refresh_token': [IsAuthenticated],
        'logout': [IsAuthenticated]
    }

    @action(detail=True, methods=['patch'])
    def block_user(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not user.is_blocked:
            user.is_blocked = True
            user.save(update_fields=["is_blocked", "unblock_date"])
            return Response("The user has blocked!")
        else:
            return Response("The user is already blocked!")

    @action(detail=False, methods=['post'])
    def register(self, request):
        user = request.data
        serializer = UserSignUpSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }
        return response

    @action(detail=False, methods=['post'])
    def refresh_token(self, request: Request):
        refresh_token = request.COOKIES.get('refresh_token')
        payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        user = User.objects.filter(id=payload.get('user_id')).first()
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})

    @action(detail=False, methods=['post'])
    def logout(self, request: Request):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refreshtoken")
        response.delete_cookie("refresh_token")
        response.data = {
            "message": "Logout successfully!"
        }
        return response

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
