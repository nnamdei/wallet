from ....lib.api.app_response import AppResponse
from ....utils.constants import NOOB, ELITE, FUND, WITHDRAW
from .transaction_model import Transaction
from ..wallet.wallet_model import Wallet
from ..auth.auth_model import Auth
from ....lib.api.flask_error import BadRequest
from ....utils.constants import BAD_REQUEST, FORBIDDEN
import pydash
from mongoengine.errors import DoesNotExist
from flask_jwt_extended import get_jwt_identity


class TransactionProcessor:
    @staticmethod
    def process_object(obj, auth_id=None):
        payload = {}
        elite_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.elite
        noob_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.noob
        admin_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.admin

        if elite_authorized:
            payload = {'user': get_jwt_identity(), 'approval_status': True, 'user_type': ELITE}
        if noob_authorized:
            payload = {'user': get_jwt_identity(), 'approval_status': False, 'user_type': NOOB}
        if admin_authorized and auth_id:
            user_info = Auth.objects.get(id=auth_id)
            payload = {'user': auth_id, 'approval_status': True, 'user_type': user_info.user_type}
        return pydash.assign(obj, payload)

    @staticmethod
    def post_approval_object(obj, data):
        return pydash.assign(obj,
                             {'amount': data.amount,
                              'transaction_type': data.transaction_type,
                              'currency': data.currency,
                              'user_type': NOOB
                              })

    @staticmethod
    def transaction_user_funding_check(obj):
        admin_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.admin
        elite_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.elite
        noob_authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.noob
        if admin_authorized:
            raise BadRequest('Operation not allowed', FORBIDDEN)
        wallet_info = TransactionProcessor.get_wallet_details(get_jwt_identity(), obj)
        if noob_authorized and obj['transaction_type'] == WITHDRAW and wallet_info.balance < obj['amount']:
            raise BadRequest('Insufficient balance', BAD_REQUEST)
        if elite_authorized and obj['transaction_type'] == WITHDRAW:
            try:
                main_wallet_balance, main_currency = TransactionProcessor.get_main_wallet_balance(get_jwt_identity())
                if wallet_info.balance < obj['amount'] and main_wallet_balance < obj['amount']:
                    raise BadRequest('Insufficient balance', BAD_REQUEST)
            except Exception as e:
                print(str(e))
                raise BadRequest('Please fund the specified wallet', BAD_REQUEST)

    @staticmethod
    def transaction_error_check(obj):
        authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.admin
        if authorized is False:
            raise BadRequest('Access forbidden', FORBIDDEN)
        if authorized and obj['transaction_type'] == WITHDRAW:
            raise BadRequest('Operation not allowed', FORBIDDEN)

    @staticmethod
    def transaction_approval_check(auth_id, trans_id):
        authorized: bool = Auth.objects.get(id=get_jwt_identity()).access.admin
        user_authorized: bool = Auth.objects.get(id=auth_id).access.noob
        print(trans_id, auth_id)
        trans_info = Transaction.objects.get(id=trans_id, user=auth_id)
        if authorized is False and user_authorized is False:
            raise BadRequest('Operation not allowed', FORBIDDEN)
        if authorized and user_authorized and trans_info.approval_status:
            raise BadRequest('Transaction already approved', BAD_REQUEST)

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
    def get_wallet_details(user, obj):
        print(user, obj)
        try:
            wallet_info = Wallet.objects.get(user=user, currency=obj['currency'])
            return wallet_info
        except DoesNotExist:
            main_wallet_currency = TransactionProcessor.main_wallet_currency(user)
            wallet_info = Wallet.objects.get(user=user, currency=main_wallet_currency.main_currency)
            return wallet_info

    @staticmethod
    def count_wallet_object(auth_id):
        return Wallet.objects(user=auth_id).count()

    @staticmethod
    def update_wallet(auth_id, currency, obj):
        return Wallet.objects(user=auth_id,currency=currency).update(**obj)

    @staticmethod
    def main_wallet_currency(user):
        return Auth.objects.get(id=user)

    @staticmethod
    def get_main_wallet_balance(user):
        request = TransactionProcessor.main_wallet_currency(user)
        main_wallet_currency = request.main_currency
        main_wallet_info = TransactionProcessor.get_wallet_details(user,
                                                                   {'currency': main_wallet_currency})
        return main_wallet_info.balance, main_wallet_currency

    @staticmethod
    def create_wallet(auth_id, obj):
        balance = 0
        if 'amount' in obj:
            balance = obj['amount']
        data = pydash.assign({}, {'user': auth_id, 'balance': balance, 'currency': obj['currency'], 'active': True})
        wallet = Wallet(**data)
        wallet.save()

    @staticmethod
    def process_withdrawal(wallet_info, obj):
        balance = wallet_info.balance
        currency = obj['currency']
        main_wallet_balance, main_currency = TransactionProcessor.get_main_wallet_balance(obj['user'])
        if wallet_info.balance < obj['amount'] and main_wallet_balance < obj['amount']:
            raise BadRequest('Insufficient funds', BAD_REQUEST)
        if balance < obj['amount']:
            balance = main_wallet_balance
            currency = main_currency
        return balance, currency

    @staticmethod
    def noob_wallet(auth_id, obj):
        try:
            wallet_info = TransactionProcessor.get_wallet_details(auth_id, obj)
            print(wallet_info.balance)
            balance = wallet_info.balance - obj['amount']
            if obj['transaction_type'] == FUND:
                balance = wallet_info.balance + obj['amount']
            TransactionProcessor.update_wallet(auth_id, wallet_info.currency, {'balance': balance})
        except DoesNotExist:
            TransactionProcessor.update_wallet(auth_id, obj)

    @staticmethod
    def elite_wallet(auth_id, obj):
        try:
            print('creating wallet')
            wallet_info = TransactionProcessor.get_wallet_details(auth_id, obj)

            if obj['transaction_type'] == WITHDRAW:
                new_balance, currency = TransactionProcessor.process_withdrawal(wallet_info, obj)
                balance = new_balance - obj['amount']
            if obj['transaction_type'] == FUND:
                balance = wallet_info.balance + obj['amount']
                currency = obj['currency']
            result = TransactionProcessor.update_wallet(auth_id, currency, {'balance': balance})
            if result == 0:
                TransactionProcessor.create_wallet(auth_id, obj)
        except DoesNotExist:
            TransactionProcessor.create_wallet(auth_id, obj)

    @staticmethod
    def process_wallet(auth_id, obj):
        if obj['user_type'] == NOOB and obj['approval_status'] == True:
            print(obj)
            TransactionProcessor.noob_wallet(auth_id, obj)
        if obj['user_type'] == ELITE:
            TransactionProcessor.elite_wallet(auth_id, obj)

