from flask_restful import Resource
from flask import request
import json
from flask_jwt_extended import jwt_required

from ....lib.api.flask_error import BadRequest
from ....utils.constants import OK, BAD_REQUEST
from ..auth.auth_model import Auth
from .user_processor import UserProcessor


class User(Resource):
    @staticmethod
    @jwt_required()
    def get():
        try:
            auth = Auth.objects()
            response = UserProcessor.get_response({
                'code': OK,
                'value': json.loads(auth.to_json())
            })
            return response, OK
        except Exception as e:
            print(type(e))
            raise BadRequest(str(e), BAD_REQUEST)


class DemoteUser(Resource):
    @staticmethod
    @jwt_required()
    def put(user_id: str):
        try:
            data = request.json
            UserProcessor.admin_authorization_check()
            UserProcessor.demote_error_check(user_id)
            processed_object = UserProcessor.process_demote_object(data)
            Auth.objects(id=user_id).update(**processed_object)
            response = UserProcessor.get_response({
                'code': OK,
                'message': 'SUCCESS',
                'value': ''
            })
            return response, OK
        except Exception as e:
            print(type(e))
            raise BadRequest(str(e), BAD_REQUEST)


class ChangeCurrency(Resource):
    @staticmethod
    @jwt_required()
    def put(user_id: str):
        try:
            data = request.json
            UserProcessor.admin_authorization_check()
            Auth.objects(id=user_id).update(**{'main_currency': data['currency']})
            response = UserProcessor.get_response({
                'code': OK,
                'message': 'SUCCESS',
                'value': ''
            })
            return response, OK
        except Exception as e:
            print(type(e))
            raise BadRequest(str(e), BAD_REQUEST)