import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.conversation_endpoint import ConversationsEndpoint
from src.api.api_exceptions import DatabaseException
from src.api import api

class TestConversationsEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(ConversationsEndpoint, '/conversations/<string:uid>')
        self.client = self.app.test_client()

    @patch('src.api.endpoints.conversation_endpoint.get_conversations')
    def test_get_success(self, mock_get_conversations):
        """Test the GET method for a successful response."""
        mock_get_conversations.return_value = [
            {"id": "conv1", "title": "Conversation 1"},
            {"id": "conv2", "title": "Conversation 2"}
        ]

        response = self.client.get('/conversations/test_uid')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "success",
            "conversations": [
                {"id": "conv1", "title": "Conversation 1"},
                {"id": "conv2", "title": "Conversation 2"}
            ]
        })
        mock_get_conversations.assert_called_once_with("test_uid")

    @patch('src.api.endpoints.conversation_endpoint.get_conversations')
    def test_get_database_exception(self, mock_get_conversations):
        """Test the GET method when DatabaseException is raised."""
        mock_get_conversations.side_effect = DatabaseException("Database access error.", code=500)

        response = self.client.get('/conversations/test_uid')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_get_conversations.assert_called_once_with("test_uid")

    @patch('src.api.endpoints.conversation_endpoint.get_conversations')
    def test_get_type_error(self, mock_get_conversations):
        """Test the GET method when TypeError is raised."""
        mock_get_conversations.side_effect = TypeError("Type error.")

        response = self.client.get('/conversations/test_uid')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_get_conversations.assert_called_once_with("test_uid")

    @patch('src.api.endpoints.conversation_endpoint.get_conversations')
    def test_get_generic_exception(self, mock_get_conversations):
        """Test the GET method when a generic exception is raised."""
        mock_get_conversations.side_effect = Exception("Generic error.")

        response = self.client.get('/conversations/test_uid')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_get_conversations.assert_called_once_with("test_uid")

if __name__ == '__main__':
    unittest.main()