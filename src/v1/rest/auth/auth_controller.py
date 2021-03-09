from flask_restful import Resource
from flask import request
import json
from ....utils.constants import ADMIN, NOOB, ELITE
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist
import pydash

from ....lib.api.flask_error import BadRequest
from ....utils.constants import OK, BAD_REQUEST
from .auth_model import Auth
from .auth_processor import AuthProcessor
from ..wallet.wallet_processor import WalletProcessor


class Register(Resource):
    @staticmethod
    def post():
        data = request.json
        try:
            auth = Auth.objects.get(email=data['email'])
            if auth:
                AuthProcessor.can_signup(auth)
        except DoesNotExist:
            pass
        processed_object = AuthProcessor.process_signup_object(data)
        print(processed_object)
        auth = Auth(**processed_object)
        auth.save()
        if data['user_type'] != ADMIN:
            WalletProcessor.create_wallet(str(auth.id), data)
        response = AuthProcessor.get_response({
            'code': OK,
            'value': json.loads(auth.to_json())
        })
        return response, OK


class Login(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()
            auth = Auth.objects.get(email=data.get('email'))
            AuthProcessor.can_login(auth, data)
            processed_obj = AuthProcessor.process_object(auth)
            response = AuthProcessor.get_response({
                'code': OK,
                'token': processed_obj['token'],
                'value': pydash.omit(processed_obj, 'token')
            })
            return response, OK
        except Exception as e:
            raise BadRequest(str(e), BAD_REQUEST)