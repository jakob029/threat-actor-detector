import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.ollama_endpoint import Analyzis
from src.api.api_exceptions import DatabaseException, UNKNOWN_ISSUE
from ollama import ResponseError
from httpx import ConnectTimeout
from src.api import api


class TestAnalyzisPost(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Analyzis, "/analysis")
        self.client = self.app.test_client()

    @patch("src.api.endpoints.ollama_endpoint.construct_analyze_prompt")
    @patch("src.api.endpoints.ollama_endpoint.send_analyze_prompt")
    @patch("src.api.endpoints.ollama_endpoint.set_graph_to_conversation")
    @patch("src.api.endpoints.ollama_endpoint.add_message")
    @patch("src.api.endpoints.ollama_endpoint.SchemaParser.correct_structure")
    @patch("src.api.endpoints.ollama_endpoint.llama_json_parser")
    def test_post_success(
        self,
        mock_llama_json_parser,
        mock_correct_structure,
        mock_add_message,
        mock_set_graph,
        mock_send_prompt,
        mock_construct_analyze_prompt,
    ):
        """Test the POST method for a successful response."""
        mock_construct_analyze_prompt.return_value = "constructed_prompt"
        mock_send_prompt.return_value = "response"
        mock_llama_json_parser.return_value = "parsed_response"
        mock_correct_structure.return_value = "statistics"

        response = self.client.post("/analysis", json={"prompt": "example_prompt", "cid": "test_cid"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "success", "response": "response", "data_points": "statistics"})
        mock_send_prompt.assert_called_once_with("constructed_prompt")

    @patch("src.api.endpoints.ollama_endpoint.construct_analyze_prompt")
    def test_post_response_error(self, mock_send_prompt):
        """Test the POST method when ResponseError is raised."""
        mock_send_prompt.side_effect = ResponseError("Response error.")

        response = self.client.post("/analysis", json={"prompt": "example_prompt", "cid": "test_cid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Internal Server Error"})
        mock_send_prompt.assert_called_once_with("example_prompt", "test_cid")

    @patch("src.api.endpoints.ollama_endpoint.construct_analyze_prompt")
    def test_post_connect_timeout(self, mock_send_prompt):
        """Test the POST method when ConnectTimeout is raised."""
        mock_send_prompt.side_effect = ConnectTimeout("Connection timed out.")

        response = self.client.post("/analysis", json={"prompt": "example_prompt", "cid": "test_cid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Internal Server Error"})
        mock_send_prompt.assert_called_once_with("example_prompt", "test_cid")

    @patch("src.api.endpoints.ollama_endpoint.construct_analyze_prompt")
    def test_post_type_error(self, mock_send_prompt):
        """Test the POST method when TypeError is raised."""
        mock_send_prompt.side_effect = TypeError("Type error.")

        response = self.client.post("/analysis", json={"prompt": "example_prompt", "cid": "test_cid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Internal Server Error"})
        mock_send_prompt.assert_called_once_with("example_prompt", "test_cid")

    @patch("src.api.endpoints.ollama_endpoint.construct_analyze_prompt")
    def test_post_database_exception(self, mock_send_prompt):
        """Test the POST method when DatabaseException is raised."""
        mock_send_prompt.side_effect = DatabaseException("Database access error.", code=UNKNOWN_ISSUE)

        response = self.client.post("/analysis", json={"prompt": "example_prompt", "cid": "test_cid"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Internal Server Error"})
        mock_send_prompt.assert_called_once_with("example_prompt", "test_cid")
