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
            return validate_jwt_token(request, User, refresh_token)
        else:
            authorization_header = request.headers.get('Authorization', None)
            access_token = authorization_header.split(' ')[1]
            logger.info(f"Request received for endpoint {str(request.path)}")
            if authorization_header:
                return validate_jwt_token(request, User, access_token)
            else:
                response = create_response(
                    "", 401, {"message": "Authorization not found, Please send valid token in headers"}
                )
                logger.info(f"Response {response}")
                return HttpResponse(json.dumps(response), status=401)
