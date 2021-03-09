
def user_noob_object():
    return {
        'email': 'john@yahoo.com',
        'password': 'helloworld123',
        'currency': 'NGN',
        'user_type': 'noob',
        'access': {
            "noob": True,
            "elite": False,
            "admin": False
        }
    }

def user_elite_object():
   return {
        'email': 'nnamdi0@gmail.com',
        'password': 'bingo1234',
        'currency': 'NGN',
        'user_type': 'elite',
        'access': {
            "noob": False,
            "elite": True,
            "admin": False
        }
    }

def user_admin_object():
return {
        'email': 'nnamdi0@mail.com',
        'password': 'software',
        'currency': 'NGN',
        'user_type': 'admin',
        'access': {
            "noob": False,
            "elite": False,
            "admin": True
        }
    }