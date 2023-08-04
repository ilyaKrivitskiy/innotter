import datetime
import json
import logging
import jwt
from django.conf import settings
from django.http import HttpResponse
from rest_framework import exceptions

logger = logging.getLogger(__name__)


def create_response(request_id, code, message):

    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')


def validate_jwt_token(request, user, authorization_header):
    try:
        access_token = authorization_header.split(' ')[1]
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_by_id = user.objects.filter(id=payload['user_id']).first()
        if user_by_id is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user_by_id.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        return None

    except jwt.ExpiredSignatureError:
        response = create_response("", 401, {"message": "Authentication token has expired"})
        logger.info(f"Response {response}")
        return HttpResponse(json.dumps(response), status=401)
    except IndexError:
        response = create_response("", 401, {"message": "Authorization has failed, Please send valid token."})
        logger.info(f"Response {response}")
        return HttpResponse(json.dumps(response), status=401)


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=15),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    print("checkpoint rt 1")
    print(type(refresh_token_payload), type(settings.REFRESH_TOKEN_SECRET))
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
    return refresh_token
