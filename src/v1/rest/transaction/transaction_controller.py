from flask_restful import Resource
from flask import request
from mongoengine import ObjectIdField
import json
import pydash
from bson.objectid import ObjectId
from ....lib.api.flask_error import BadRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from ....utils.constants import OK, BAD_REQUEST
from .transaction_model import Transaction
from .transaction_processor import TransactionProcessor


class TransactionPayment(Resource):
    @staticmethod
    @jwt_required()
    def post():
        data = request.json
        TransactionProcessor.transaction_user_funding_check(data)
        print('passed here')
        processed_object = TransactionProcessor.process_object(data)
        transaction = Transaction(**pydash.omit(processed_object, 'user_type'))
        transaction.save()
        TransactionProcessor.process_wallet(get_jwt_identity(), data)
        response = TransactionProcessor.get_response({
            'code': OK,
            'value': json.loads(transaction.to_json())
        })
        return response, OK


class AdminTransactionPayment(Resource):
    @staticmethod
    @jwt_required()
    def post(user_id: str):
        data = request.json
        TransactionProcessor.transaction_error_check(data)
        processed_object = TransactionProcessor.process_object(data, auth_id=user_id)
        transaction = Transaction(**pydash.omit(processed_object, 'user_type'))
        transaction.save()
        TransactionProcessor.process_wallet(user_id, data)
        response = TransactionProcessor.get_response({
            'code': OK,
            'value': json.loads(transaction.to_json())
        })
        return response, OK


class AdminTransactionApproval(Resource):
    @staticmethod
    @jwt_required()
    def post(transaction_id: str):
        data = request.json
        auth_id = data['auth_id']
        print(auth_id)
        TransactionProcessor.transaction_approval_check(auth_id, transaction_id)
        processed_object = TransactionProcessor.process_object(data, auth_id=auth_id)
        processed_object = pydash.omit(processed_object, 'auth_id')
        processed_object = pydash.omit(processed_object, 'user')
        Transaction.objects(id=transaction_id).update(**processed_object)
        transaction = Transaction.objects.get(id=transaction_id)
        print(transaction.amount)
        post_object = TransactionProcessor.post_approval_object(data, transaction)
        TransactionProcessor.process_wallet(auth_id, post_object)
        response = TransactionProcessor.get_response({
            'code': OK,
            'value': json.loads(transaction.to_json())
        })
        return response, OK
            # raise BadRequest(str(e), BAD_REQUEST)