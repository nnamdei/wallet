from ....lib.api.app_response import AppResponse
from flask_jwt_extended import create_access_token, create_refresh_token
from ....lib.api.flask_error import BadRequest
from ....utils.constants import UNAUTHORIZED, NOT_FOUND, BAD_REQUEST
import pydash
import datetime


class AuthProcessor:
    @staticmethod
    def process_object(auth):
        expiry = datetime.timedelta(days=5)
        access_token = create_access_token(identity=str(auth.id), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(auth.id))
        new_object = pydash.assign({}, {
            'token': access_token,
            'refresh': refresh_token,
            'email': f"{auth.email}",
            'active': f"{auth.active}"
        })
        return new_object

    @staticmethod
    def process_signup_object(obj):
        obj['main_currency'] = obj.pop('currency')
        return obj

    @staticmethod
    def get_response(obj):
        print(obj)
        meta = AppResponse.get_success_meta()
        if 'token' in obj:
            meta['token'] = obj['token']
        pydash.assign(meta, {'status_code': obj['code']})
        if 'message' in obj:
            meta['message'] = obj['message']
        return AppResponse.format(meta, obj['value'])

    @staticmethod
    def can_login(auth, obj):
        if auth is None:
            raise BadRequest('User not found', NOT_FOUND)
        if not auth.check_pw_hash(obj.get('password')):
            raise BadRequest('Incorrect password', UNAUTHORIZED, {'ext': 1})

    @staticmethod
    def can_signup(auth):
        if auth.email:
            raise BadRequest('Email already exist', BAD_REQUEST)


