"""Unittest for API message endpoint."""

import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.message_endpoint import MessagesEndpoint
from src.api.api_exceptions import DatabaseException, CONVERSATION_DOES_NOT_EXIST


class TestMessagesEndpoint(unittest.TestCase):
    """Test class for API messages endpoint get delete methods."""

    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(MessagesEndpoint, "/messages/<string:cid>")
        self.client = self.app.test_client()

    @patch("src.api.endpoints.message_endpoint.reset_conversation")
    def test_delete_success(self, mock_reset_conversation):
        """Test the DELETE method for a successful response."""
        response = self.client.delete("/messages/test_cid")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "success"})
        mock_reset_conversation.assert_called_once_with("test_cid")

    @patch("src.api.endpoints.message_endpoint.reset_conversation")
    def test_delete_database_exception(self, mock_reset_conversation):
        """Test the DELETE method when DatabaseException is raised."""
        mock_reset_conversation.side_effect = DatabaseException(
            "Database access error.", code=CONVERSATION_DOES_NOT_EXIST
        )

        response = self.client.delete("/messages/test_cid")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Database access error."})
        mock_reset_conversation.assert_called_once_with("test_cid")

    @patch("src.api.endpoints.message_endpoint.reset_conversation")
    def test_delete_generic_exception(self, mock_reset_conversation):
        """Test the DELETE method when a generic exception is raised."""
        mock_reset_conversation.side_effect = Exception("Generic error.")

        response = self.client.delete("/messages/test_cid")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "something went wrong."})
        mock_reset_conversation.assert_called_once_with("test_cid")
