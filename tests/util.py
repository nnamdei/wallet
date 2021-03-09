from src.v1.rest.auth.auth_model import Auth
from src.v1.rest.wallet.wallet_model import Wallet


def empty_auth_collection():
    Auth.drop_collection()


def empty_wallet_collection():
    Wallet.drop_collection()