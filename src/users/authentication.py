import jwt
from config.settings import SECRET_KEY
from .models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        action_method = request.path.split('/')[-1]
        if action_method in ("register", "login"):
            return None
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            access_token_payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('No such user')

        user = User.objects.filter(id=access_token_payload['user_id']).first()
        return (user, None)
