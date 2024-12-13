import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from argon2.exceptions import VerifyMismatchError
from src.api import api
from src.api.endpoints.user_endpoint import Authentication
from src.api.api_exceptions import (
    AuthenticationException,
    DatabaseException,
    USERNAME_TOO_LONG,
    USER_DOES_NOT_EXIST,
    VARIABLE_NOT_SET,
    UNKNOWN_ISSUE,
)

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Authentication, '/auth')
        self.client = self.app.test_client()

    @patch('src.api.endpoints.user_endpoint.authenicate')
    def test_post_success(self, mock_authenticate):
        """Test the POST method for a successful authentication."""
        mock_authenticate.return_value = "user_id"

        response = self.client.post('/auth', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "success", "uid": "user_id"})
        mock_authenticate.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.authenicate')
    def test_post_authentication_exception(self, mock_authenticate):
        """Test the POST method when AuthenticationException is raised."""
        mock_authenticate.side_effect = AuthenticationException("Authentication failed.", code=USERNAME_TOO_LONG)

        response = self.client.post('/auth', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Password or User is wrong."})
        mock_authenticate.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.authenicate')
    def test_post_database_exception(self, mock_authenticate):
        """Test the POST method when DatabaseException is raised."""
        mock_authenticate.side_effect = DatabaseException("Database error.", code=VARIABLE_NOT_SET)

        response = self.client.post('/auth', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Something went wrong."})
        mock_authenticate.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.authenicate')
    def test_post_verify_mismatch_error(self, mock_authenticate):
        """Test the POST method when VerifyMismatchError is raised."""
        mock_authenticate.side_effect = VerifyMismatchError

        response = self.client.post('/auth', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Password or User is wrong."})
        mock_authenticate.assert_called_once_with("test_user", "test_pass")

    @patch('src.api.endpoints.user_endpoint.authenicate')
    def test_post_generic_exception(self, mock_authenticate):
        """Test the POST method when a generic exception is raised."""
        mock_authenticate.side_effect = Exception("Generic error.")

        response = self.client.post('/auth', json={"username": "test_user", "password": "test_pass"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Something went wrong"})
        mock_authenticate.assert_called_once_with("test_user", "test_pass")

if __name__ == '__main__':
    unittest.main()