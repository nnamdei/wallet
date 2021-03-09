from flask import Blueprint
from flask_restful import Api
from default import Home


class RouteHandler:

    def __init__(self, flask_app):
        self.flask = flask_app
        self.api = Api(self.flask)

    def setup(self):
        from src.v1.rest.auth.auth_route import Router
        from src.v1.rest.user.user_route import UserRouter
        from src.v1.rest.wallet.wallet_route import WalletRouter
        from src.v1.rest.transaction.transaction_route import TransactionRouter
        bp = Blueprint('api', __name__)
        admin_bp = Blueprint('admin', __name__)
        api = Api(bp)
        Router(api)
        UserRouter(api)
        WalletRouter(api)
        TransactionRouter(api)

        self.flask.register_blueprint(bp, url_prefix="/api/v1")

        self.flask.register_blueprint(admin_bp, url_prefix="/api/v1/admin")
        self.api.add_resource(Home, '/')
