from flask_restful import Resource
import json
from flask_jwt_extended import jwt_required, get_jwt_identity

from ....lib.api.flask_error import BadRequest
from ....utils.constants import OK, BAD_REQUEST
from .wallet_model import Wallet
from .wallet_processor import WalletProcessor


class UserWallet(Resource):
    @staticmethod
    @jwt_required()
    def get():
        try:
            wallet = Wallet.objects(user=get_jwt_identity())
            response = WalletProcessor.get_response({
                'code': OK,
                'value': json.loads(wallet.to_json())
            })
            return response, OK
        except Exception as e:
            print(type(e))
            raise BadRequest(str(e), BAD_REQUEST)


class UserWalletStatus(Resource):
    @staticmethod
    @jwt_required()
    def put(user_id: str):
        try:
            WalletProcessor.authorization_check()
            wallet = Wallet.objects(id=user_id).update(**{'active': True})
            response = WalletProcessor.get_response({
                'code': OK,
                'value': json.loads(wallet.to_json())
            })
            return response, OK
        except Exception as e:
            print(type(e))
            raise BadRequest(str(e), BAD_REQUEST)