from mongoengine import *
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
from .... import Database
import bcrypt

class Access(EmbeddedDocument):
    """
    Custom EmbeddedDocument to set user authorizations.
    :param noob: boolean value to signify if user is a user
    :param admin: boolean value to signify if user is an admin
    """
    noob = BooleanField(default=True)
    elite = BooleanField(default=True)
    admin = BooleanField(default=False)


class Auth(Document):
    email = EmailField(max_length=200, required=True)
    password = StringField(min_length=8, required=True)
    access = EmbeddedDocumentField(Access, default=Access(noob=True, elite=False, admin=False))
    user_type = StringField(required=True)
    main_currency = StringField(required=True)
    active = BooleanField(default=True)

    def generate_pw_hash(self):
        self.password = generate_password_hash(password=self.password).decode('utf-8')
    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)
    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_pw_hash()
        super(Auth, self).save(*args, **kwargs)
