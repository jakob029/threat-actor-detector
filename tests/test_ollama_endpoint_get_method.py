
import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from src.api.endpoints.ollama_endpoint import Analyzis
from src.api.api_exceptions import DatabaseException
from src.api import api

class TestAnalyzisGet(unittest.TestCase):
    def setUp(self):
        """Set up Flask test app and API."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Analyzis, '/analysis/<string:cid>')
        self.client = self.app.test_client()

    @patch('src.api.endpoints.ollama_endpoint.get_graph')
    def test_get_success(self, mock_get_graph):
        """Test the GET method for a successful response."""
        # Mock return value for get_graph
        mock_get_graph.return_value = [{"key": "value"}]

        response = self.client.get('/analysis/test_cid')

        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "success",
            "data_points": [{"key": "value"}]
        })

        # Ensure get_graph was called with the correct CID
        mock_get_graph.assert_called_once_with("test_cid")

    @patch('src.api.endpoints.ollama_endpoint.get_graph')
    def test_get_database_exception(self, mock_get_graph):
        """Test the GET method when DatabaseException is raised."""
        # Mock DatabaseException for get_graph
        mock_get_graph.side_effect = DatabaseException("Database error.", code=500)

        response = self.client.get('/analysis/test_cid')

        # Validate response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Something went wrong."})

        # Ensure get_graph was called with the correct CID
        mock_get_graph.assert_called_once_with("test_cid")

    @patch('src.api.endpoints.ollama_endpoint.get_graph')
    def test_get_generic_exception(self, mock_get_graph):
        """Test the GET method when a generic exception is raised."""
        # Mock generic Exception for get_graph
        mock_get_graph.side_effect = Exception("Unexpected error.")

        response = self.client.get('/analysis/test_cid')

        # Validate response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Something went wrong."})

        # Ensure get_graph was called with the correct CID
        mock_get_graph.assert_called_once_with("test_cid")


if __name__ == '__main__':
    unittest.main()