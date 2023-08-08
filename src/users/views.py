import jwt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from config.settings import SECRET_KEY, REFRESH_TOKEN_SECRET
from .serializers import UserSerializer, UserSignUpSerializer
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from .authentication import JWTAuthentication
from .models import User
from pages.models import Page
from rest_framework.request import Request
from rest_framework.response import Response
from .permissions import IsSuperUser, IsOwnerOrReadOnly, IsAdminRole, IsNotBlocked
from .tokens import generate_access_token, generate_refresh_token


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("id").values()
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
        'destroy': [IsSuperUser],
        'block_user': [IsAdminRole],
        'make_user_admin': [IsSuperUser],
        'make_user_moderator': [IsAdminRole]
    }

    def perform_create(self, serializer):
        if self.request.user in ("moderator", "admin"):
            serializer.save(is_staff=True)

    @action(detail=True, methods=['patch'])
    def make_user_admin(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.role = user.Roles.ADMIN
        user.is_staff = True
        user.save()
        return Response(data="This user has admin role now!")

    @action(detail=True, methods=['patch'])
    def make_user_moderator(self, request: Request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.role = user.Roles.MODERATOR
        user.is_staff = True
        user.save()
        return Response(data="This user has moderator role now!")

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

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        user = request.data
        serializer = UserSignUpSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        user = User.objects.filter(username=username).first()
        serialized_user = UserSerializer(user).data
        if user is None:
            raise exceptions.AuthenticationFailed('Username is required! User not found.')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Password is required! Wrong Password.')

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }
        return response


class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        refresh_token = request.COOKIES.get('refresh_token')
        payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        user = User.objects.filter(id=payload.get('user_id')).first()
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.data = {
            "message": "Logout successfully!"
        }
        return response
