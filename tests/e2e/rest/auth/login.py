import json
from tests import util
from ....e2e.routes import SIGNUP, LOGIN, HEADERS
from ...rest.base import BaseCase
from ....seeds.user_seed import user_noob_object


class TestUserSignIn(BaseCase):
    def __init__(self):
        super().__init__()

    util.empty_auth_collection()

    def test_successful_wallet_details(self):
        # Given
        payload = json.dumps(user_noob_object())
        # When
        response = self.app.post(SIGNUP, headers=HEADERS, data=payload)
        print(response.json)
        # When
        response = self.app.post(LOGIN, headers=HEADERS, data=payload)
        print(response.json)
        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)