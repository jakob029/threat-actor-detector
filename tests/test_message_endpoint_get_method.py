import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.message_endpoint import MessagesEndpoint
from src.api.api_exceptions import DatabaseException, CONVERSATION_DOES_NOT_EXIST
from src.api import api

class TestMessagesEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(MessagesEndpoint, '/messages/<string:cid>')
        self.client = self.app.test_client()

    @patch('src.api.endpoints.message_endpoint.get_messages')
    def test_get_success(self, mock_get_messages):
        """Test the GET method for a successful response."""
        mock_get_messages.return_value = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "system", "content": "System message"}
        ]

        response = self.client.get('/messages/test_cid')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "success",
            "conversation_history": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        })
        mock_get_messages.assert_called_once_with("test_cid")

    @patch('src.api.endpoints.message_endpoint.get_messages')
    def test_get_database_exception(self, mock_get_messages):
        """Test the GET method when DatabaseException is raised."""
        mock_get_messages.side_effect = DatabaseException("Database access error.", code=CONVERSATION_DOES_NOT_EXIST)

        response = self.client.get('/messages/test_cid')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_get_messages.assert_called_once_with("test_cid")

    @patch('src.api.endpoints.message_endpoint.get_messages')
    def test_get_generic_exception(self, mock_get_messages):
        """Test the GET method when a generic exception is raised."""
        mock_get_messages.side_effect = Exception("Generic error.")

        response = self.client.get('/messages/test_cid')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_get_messages.assert_called_once_with("test_cid")

if __name__ == '__main__':
    unittest.main()