import unittest
from base64 import b64encode

from app.resources.foo import Foo
from app import create_app
from config import Config

class TestAPI(unittest.TestCase):

    def setUp(self):
        app = create_app(Config)
        app.app_context().push()
        self.test_client = app.test_client()

    def test_api_returns_401_with_no_authorization(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status_code, 401)

    def test_api_returns_401_with_invalid_username(self):
        response = self.test_client.get('/', headers={'Authorization': b'Basic ' + b64encode(b'invalid_user:pass')})
        self.assertEqual(response.status_code, 401)

    def test_api_returns_401_with_invalid_password(self):
        response = self.test_client.get('/', headers={'Authorization': b'Basic ' + b64encode(b'test_user:invalid_pass')})
        self.assertEqual(response.status_code, 401)

    def test_api_returns_200_with_valid_authorization(self):
        response = self.test_client.get('/', headers={'Authorization': b'Basic ' + b64encode(b'test_user:pass')})
        self.assertEqual(response.status_code, 200)
