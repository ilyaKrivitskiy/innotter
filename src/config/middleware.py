import logging
import jwt
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import exceptions
from rest_framework.utils import json
from users.models import User
from config.settings import SECRET_KEY, REFRESH_TOKEN_SECRET
from users.tokens import validate_jwt_token, create_response

logger = logging.getLogger(__name__)


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        action_method = request.path.split('/')[-1]

        if action_method in ("register", "login"):
            return None
        elif action_method == 'refresh':
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                raise exceptions.AuthenticationFailed(
                    'Authentication credentials were not provided.')
            try:
                payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
                user = User.objects.filter(id=payload.get('user_id')).first()
                if user is None:
                    raise exceptions.AuthenticationFailed('User not found')

                if not user.is_active:
                    raise exceptions.AuthenticationFailed('User is inactive')
                return None
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('expired refresh token, please login again.')
        else:
            authorization_header = request.headers.get('Authorization', None)
            logger.info(f"Request received for endpoint {str(request.path)}")
            if authorization_header:
                return validate_jwt_token(request, User, authorization_header)
            else:
                response = create_response(
                    "", 401, {"message": "Authorization not found, Please send valid token in headers"}
                )
                logger.info(f"Response {response}")
                return HttpResponse(json.dumps(response), status=401)
