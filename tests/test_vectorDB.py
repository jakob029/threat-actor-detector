"""Test the functionality for the vector DB setup & API."""

import unittest
import unittest.mock as um
from src.vector_db_api.endpoints.group_analyzer import GroupAnalyzer


class collection_emulator:
    """Emulate the collection query function."""

    @staticmethod
    def query(query_texts: str, n_results: int, include: list):
        """Emulate the collection query function."""
        if query_texts and n_results and include:
            return "Test response"

        return "Incorrect response"


class build_vector_emulator:
    """Emulate Chroma DB collection."""

    collection = collection_emulator()


class TestGroupAnalyzer(unittest.TestCase):
    """Test the functionality of the GroupAnalyzer endpoint."""

    @um.patch.object(GroupAnalyzer, "__init__")
    @um.patch("flask_restful.reqparse.RequestParser.parse_args")
    def test_get(self, parse_args, mocked_constructor):
        """Test the HTTP GET method for the GroupAnalyzer endpoint."""
        mocked_constructor.return_value = None

        endpoint_instance = GroupAnalyzer()
        endpoint_instance.vector_databases = ("vector", "db")

        endpoint_instance.vector_databases = (build_vector_emulator(),)
        parse_args.return_value = {"prompt": "This is the prompt."}
        assert endpoint_instance.get() == ({"response": "Test response"}, 200)
