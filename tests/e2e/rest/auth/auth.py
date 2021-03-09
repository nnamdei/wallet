import json
from ....util import empty_auth_collection, empty_wallet_collection
from ....e2e.routes import SIGNUP, HEADERS
from ...rest.base import BaseCase
from ....seeds.user_seed import user_noob_object


class TestUserSignup(BaseCase):
    def __init__(self):
        super().__init__()

        empty_auth_collection()
        empty_wallet_collection()

    def test_successful_signup(self):
        # Given
        payload = json.dumps(user_noob_object())

        # When
        response = self.app.post(SIGNUP, headers=HEADERS, data=payload)
        print(response.json)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_signup_with_existing_field(self):
        #Given
        payload = json.dumps(user_noob_object())

        #When
        response = self.app.post(SIGNUP, headers=HEADERS, data=payload)

        # Then
        self.assertEqual('Email already exist', response.json['message'])
        self.assertEqual(400, response.status_code)
