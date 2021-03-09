class AuthError:

    def can_login(self):
        pass


class NotFound(AuthError):

    def can_login(self, auth):
        return{
            'success': False,
            'message': 'User not found'
        }


class PasswordMismatch(AuthError):

    def can_login(self, auth):
        return {
            'success': False,
            'message': 'Incorrect password'
        }