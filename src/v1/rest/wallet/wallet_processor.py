from ....lib.api.app_response import AppResponse
from ....utils.constants import ADMIN
from .wallet_model import Wallet
from ..auth.auth_model import Auth
from ....lib.api.flask_error import BadRequest
from ....utils.constants import OK, BAD_REQUEST, FORBIDDEN
import pydash
from flask_jwt_extended import jwt_required, get_jwt_identity


class WalletProcessor:
    @staticmethod
    def authorization_check():
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

    @staticmethod
    def create_wallet(auth_id, obj):
        # wallet_count = Wallet.objects.count(user=auth_id)
        print(obj)
        try:
            if obj['user_type'] != ADMIN:
                data = pydash.assign({}, {'user': auth_id, 'currency': obj['main_currency'], 'active': True})
                wallet = Wallet(**data)
                wallet.save()
        except Exception as e:
            raise BadRequest(str(e), BAD_REQUEST)



