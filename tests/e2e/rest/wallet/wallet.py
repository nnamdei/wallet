import json
from tests import util
from ....e2e.routes import WALLET, LOGIN, SIGNUP, HEADERS
from ...rest.base import BaseCase
from ....seeds.user_seed import user_noob_object


class TestUserWallet(BaseCase):
    def __init__(self):
        super().__init__()

        util.empty_auth_collection()
        util.empty_wallet_collection()

    def test_successful_wallet_info(self):
        # When
        # Given
        payload = json.dumps(user_noob_object())
        user_payload = json.dumps({
            "email": payload['email'],
            "password": payload['password']
        })
        # When
        self.app.post(SIGNUP, headers=HEADERS, data=payload)

        response = self.app.post(LOGIN, headers=HEADERS, data=user_payload)
        login_token = response.json['access_token']
        HEADERS["Authorization"] = f"Bearer {login_token}"

        response = self.app.get(WALLET, headers=HEADERS)
        print(response.json)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)