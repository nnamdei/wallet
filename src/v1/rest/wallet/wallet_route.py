from .wallet_controller import UserWallet, UserWalletStatus


class WalletRouter:
    def __init__(self, api):
        api.add_resource(UserWallet, '/wallet')
        api.add_resource(UserWalletStatus, '/wallet/<user_id>')