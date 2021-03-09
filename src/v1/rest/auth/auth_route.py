from .auth_controller import Register, Login


class Router:
    def __init__(self, api):
        api.add_resource(Register, '/signup')
        api.add_resource(Login, '/login')