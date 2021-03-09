from mongoengine import *
from ..auth.auth_model import Auth


class Transaction(Document):
    user = ReferenceField(Auth)
    amount = IntField(required=True, default=0)
    currency = StringField(required=True)
    transaction_type = StringField(required=True)
    approval_status = BooleanField(required=True, default=False)
