from base64 import b64encode
import unittest

from app import create_app, db
from app.resources.users import User

class TestConfig():
    SECRET_KEY = "123456"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()
        user = User(username="test")
        user.set_password("test")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_registration_with_valid_user_creates_new_user(self):
        self.assertEqual(User.query.count(), 1)
        response = self.test_client.post('/register', json={'username': 'new_user', 'password': 'new_user'})
        self.assertEqual(User.query.count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_registration_with_duplicate_username_returns_404(self):
        response = self.test_client.post('/register', json={'username': 'test', 'password': 'new_user'})
        self.assertEqual(response.status_code, 404)

    def test_registration_with_blank_username_returns_404(self):
        response = self.test_client.post('/register', json={'username': '', 'password': 'new_user'})
        self.assertEqual(response.status_code, 404)

    def test_registration_with_blank_password_returns_404(self):
        response = self.test_client.post('/register', json={'username': 'user', 'password': ''})
        self.assertEqual(response.status_code, 404)

    def test_get_token_with_invalid_credentials_returns_401(self):
        response = self.test_client.get('/token', headers={'Authorization': b'Basic ' + b64encode(b'test:test_invalid')})
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(response.json)

    def test_get_token_with_valid_credentials_returns_token(self):
        response = self.test_client.get('/token', headers={'Authorization': b'Basic ' + b64encode(b'test:test')})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['token'])
