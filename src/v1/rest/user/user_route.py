from .user_controller import ChangeCurrency, User, DemoteUser


class UserRouter:
    def __init__(self, api):
        api.add_resource(User, '/user')
        api.add_resource(DemoteUser, '/user/demote/<user_id>')
        api.add_resource(ChangeCurrency, '/user/currency/<user_id>')