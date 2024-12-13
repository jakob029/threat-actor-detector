import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.user_endpoint import Registration 
from src.api import api

from src.api.api_exceptions import (
    RegistrationException,
    DatabaseException,
    PASSWORD_TOO_WEAK,
    USER_ALREADY_EXIST,
    USERNAME_TOO_LONG,
)

class TestRegistration(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Registration, '/register')
        self.client = self.app.test_client()

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_success(self, mock_register):
        """Test the POST method for a successful registration."""
        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "success"})
        mock_register.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_password_too_weak(self, mock_register):
        """Test the POST method when PASSWORD_TOO_WEAK is raised."""
        mock_register.side_effect = RegistrationException("Password too weak.", code=PASSWORD_TOO_WEAK)

        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Password too weak."})
        mock_register.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_username_too_long(self, mock_register):
        """Test the POST method when USERNAME_TOO_LONG is raised."""
        mock_register.side_effect = RegistrationException("Username too long.", code=USERNAME_TOO_LONG)

        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Username too long."})
        mock_register.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_user_already_exist(self, mock_register):
        """Test the POST method when USER_ALREADY_EXIST is raised."""
        mock_register.side_effect = RegistrationException("User already exists.", code=USER_ALREADY_EXIST)

        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User already exists."})
        mock_register.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_database_exception(self, mock_register):
        """Test the POST method when DatabaseException is raised."""
        mock_register.side_effect = DatabaseException("Database access error.", code=500)

        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Something went wrong."})
        mock_register.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.register')
    def test_post_generic_exception(self, mock_register):
        """Test the POST method when a generic exception is raised."""
        mock_register.side_effect = Exception("Generic error.")

        response = self.client.post('/register', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Something went wrong."})
        mock_register.assert_called_once_with("test_user", "test_pass")

if __name__ == '__main__':
    unittest.main()