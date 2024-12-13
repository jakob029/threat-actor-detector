import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.conversation_endpoint import ConversationsEndpoint
from src.api.api_exceptions import DatabaseException, USER_DOES_NOT_EXIST
from src.api import api


class TestConversationsEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(ConversationsEndpoint, "/conversations")
        self.client = self.app.test_client()

    @patch("src.api.endpoints.conversation_endpoint.create_conversation")
    def test_post_success(self, mock_create_conversation):
        """Test the POST method for a successful response."""
        mock_create_conversation.return_value = "conversation_id"

        response = self.client.post("/conversations", json={"title": "New Conversation", "uid": "test_uid"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"messgae": "success", "conversation_id": "conversation_id"})
        mock_create_conversation.assert_called_once_with("test_uid", "New Conversation")

    @patch("src.api.endpoints.conversation_endpoint.create_conversation")
    def test_post_user_does_not_exist(self, mock_create_conversation):
        """Test the POST method when USER_DOES_NOT_EXIST is raised."""
        mock_create_conversation.side_effect = DatabaseException("User does not exist.", code=USER_DOES_NOT_EXIST)

        response = self.client.post("/conversations", json={"title": "New Conversation", "uid": "test_uid"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User does not exist."})
        mock_create_conversation.assert_called_once_with("test_uid", "New Conversation")

    @patch("src.api.endpoints.conversation_endpoint.create_conversation")
    def test_post_database_exception(self, mock_create_conversation):
        """Test the POST method when DatabaseException is raised."""
        mock_create_conversation.side_effect = DatabaseException("Database access error.", code=500)

        response = self.client.post("/conversations", json={"title": "New Conversation", "uid": "test_uid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Database access error."})
        mock_create_conversation.assert_called_once_with("test_uid", "New Conversation")

    @patch("src.api.endpoints.conversation_endpoint.create_conversation")
    def test_post_generic_exception(self, mock_create_conversation):
        """Test the POST method when a generic exception is raised."""
        mock_create_conversation.side_effect = Exception("Generic error.")

        response = self.client.post("/conversations", json={"title": "New Conversation", "uid": "test_uid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_create_conversation.assert_called_once_with("test_uid", "New Conversation")
