import jwt
import json
from aiohttp import web
from constants import *


def get_auth_token(user_id):
    return jwt.encode({user_id: AUTH.JWT_SALT}, AUTH.JWT_SECRET, algorithm='HS256').decode('utf-8')


def check_auth_token(user_id, token):
    return token == get_auth_token(user_id)


def format_user_data(user_data):
    # TODO: reconsider
    if 'birth_date' in user_data:
        user_data['birth_date'] = user_data['birth_date'].isoformat()
    return user_data


def build_response(status, data=None):
    return web.Response(text=f"{json.dumps(data)}\n", status=status)
