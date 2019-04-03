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

    def test_api_returns_401_with_no_token(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status_code, 401)

    def test_api_returns_401_with_invalid_token(self):
        response = self.test_client.get('/', headers={'Authorization': 'Bearer ' + '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8invalid'})
        self.assertEqual(response.status_code, 401)

    def test_api_returns_200_with_valid_token(self):
        response = self.test_client.get('/', headers={'Authorization': 'Bearer ' + '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'})
        self.assertEqual(response.status_code, 200)

    def test_api_returns_token_with_valid_credentials(self):
        response = self.test_client.get('/token', headers={'Authorization': b'Basic ' + b64encode(b'test_user:pass')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['token'], '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')

    def test_api_returns_401_with_invalid_credentials(self):
        response = self.test_client.get('/token', headers={'Authorization': b'Basic ' + b64encode(b'test_user:invalid')})
        self.assertEqual(response.status_code, 401)

