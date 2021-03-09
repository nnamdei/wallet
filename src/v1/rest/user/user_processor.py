from ....lib.api.app_response import AppResponse
from flask_jwt_extended import get_jwt_identity
from ....lib.api.flask_error import BadRequest
from ....utils.constants import FORBIDDEN, NOOB, ELITE
from ..auth.auth_model import Auth
import pydash


class UserProcessor:
    @staticmethod
    def process_demote_object(obj):
        values = {}
        if obj['user_type'] == NOOB:
            values = {'noob': True, 'elite': False, 'admin': False}
        if obj['user_type'] == ELITE:
            values = {'noob': False, 'elite': True, 'admin': False}
        return pydash.assign(obj, {'access': values})

    @staticmethod
    def demote_error_check(user):
        authorized: bool = Auth.objects.get(id=user).access.admin
        if authorized:
            raise BadRequest('Operation not allowed', FORBIDDEN)

    @staticmethod
    def admin_authorization_check():
        authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.admin
        if authorized is False:
            raise BadRequest('Operation not allowed', FORBIDDEN)

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

