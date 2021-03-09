from mongoengine import *
from ..auth.auth_model import Auth


class Wallet(Document):
    user = ReferenceField(Auth)
    balance = IntField(required=True, default=0)
    currency = StringField(required=True)
    active = BooleanField(default=False)
