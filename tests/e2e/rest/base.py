from ...app import app
import unittest


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()