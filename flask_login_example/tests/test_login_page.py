import unittest

from flask import url_for

from app import create_app, db
from app.models import User

class TestConfig():
    SECRET_KEY = "123456"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    WTF_CSRF_ENABLED = False


class TestLoginPage(unittest.TestCase):

    @staticmethod
    def create_user1():
        user1 = User(
            username = 'user1',
            identity = 'secret',
            alignment = 'bad',
            gender = 'genderfluid',
            sex = 'agender',
            eye_colour = 'amber',
            hair_colour = 'auburn',
            is_alive = True,
            appearances = 100)
        user1.set_password('pass1')
        return user1

    @staticmethod
    def create_registration_parameters():
        return {'RegistrationUsername': 'user2',
                'RegistrationPassword': 'pass1',
                'RegistrationPassword2': 'pass1',
                'Identity': 'secret',
                'Alignment': 'bad',
                'Gender': 'genderfluid',
                'Sex': 'agender',
                'EyeColour': 'amber',
                'HairColour': 'auburn',
                'Alive': 'Living Characters',
                'Appearances': '100'}

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()
        self.user1 = self.create_user1()
        db.session.add(self.user1)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_accessing_login_page_returns_status_code_200(self):
        response = self.test_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logging_on_with_incorrect_username_redirects_correctly(self):
        data = {'LoginUsername': 'incorrect_user', 'LoginPassword': 'pass1'}
        response = self.test_client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Username not recognised or invalid password provided - please try again' in response.data)

    def test_logging_on_with_incorrect_password_redirects_correctly(self):
        data = {'LoginUsername': 'user1', 'LoginPassword': 'incorrect_password'}
        response = self.test_client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Username not recognised or invalid password provided - please try again' in response.data)

    def test_logging_on_with_correct_details_redirects_correctly(self):
        data = {'LoginUsername': 'user1', 'LoginPassword': 'pass1'}
        response = self.test_client.post('/', data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        actual_redirect_url = response.location.split('http://localhost')[1]
        expected_redirect_url = '/index'
        self.assertEqual(actual_redirect_url, expected_redirect_url)

    def test_logged_in_user_accessing_login_page_redirects_to_index_page(self):
        data = {'LoginUsername': 'user1', 'LoginPassword': 'pass1'}
        self.test_client.post('/', data=data, follow_redirects=True)
        response = self.test_client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        actual_redirect_url = response.location.split('http://localhost')[1]
        expected_redirect_url = '/index'
        self.assertEqual(actual_redirect_url, expected_redirect_url)

    def test_cannot_access_index_page_if_not_logged_in(self):
        response = self.test_client.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_logout_redirects_to_login_page(self):
        data = {'LoginUsername': 'user1', 'LoginPassword': 'pass1'}
        self.test_client.post('/', data=data, follow_redirects=True)
        response = self.test_client.get('/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        actual_redirect_url = response.location.split('http://localhost')[1]
        expected_redirect_url = '/'
        self.assertEqual(actual_redirect_url, expected_redirect_url)

    def test_logout_logs_out_user(self):
        data = {'LoginUsername': 'user1', 'LoginPassword': 'pass1'}
        self.test_client.post('/', data=data, follow_redirects=True)
        self.test_client.get('/logout', follow_redirects=True)
        response = self.test_client.get('/index')
        self.assertEqual(response.status_code, 401)

    def test_registering_with_duplicate_username_does_not_validate(self):
        registration_parameters = TestLoginPage.create_registration_parameters()
        registration_parameters['RegistrationUsername'] = self.user1.username
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Please provide a unique username' in response.data)

    def test_registering_with_mismatched_passwords_does_not_validate(self):
        registration_parameters = TestLoginPage.create_registration_parameters()
        registration_parameters['RegistrationPassword2'] = 'mismatched_password'
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Passwords do not match" in response.data)

    def test_registering_with_invalid_appearances_argument_does_not_validate(self):
        registration_parameters = TestLoginPage.create_registration_parameters()
        registration_parameters['Appearances'] = -1
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Number must be between 1 and 9999" in response.data)
        registration_parameters['Appearances'] = 10000
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Number must be between 1 and 9999" in response.data)

    def test_registering_with_correct_details_redirects_correctly(self):
        registration_parameters = TestLoginPage.create_registration_parameters()
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        actual_redirect_url = response.location.split('http://localhost')[1]
        expected_redirect_url = '/index'
        self.assertEqual(actual_redirect_url, expected_redirect_url)

    def test_registering_with_correct_details_creates_additional_user(self):
        self.assertEqual(User.query.count(), 1)
        registration_parameters = TestLoginPage.create_registration_parameters()
        # self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        response = self.test_client.post('/', data=registration_parameters, follow_redirects=True)
        print(response.data)
        self.assertEqual(User.query.count(), 2)
