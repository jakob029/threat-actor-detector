"""Ollama requests.

Classes:
    Analyzis
"""

import os
import sys
import logging

from httpx import ConnectTimeout
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from ollama import ResponseError
from backend_connectors import send_prompt
from handlers.statistic_parser import llama_json_parser
from handlers.statistic_json_parser import SchemaParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.build_dataset.run import build_vector_database, retrieve_apt_descriptions

logger = logging.getLogger(__name__)


class Analyzis(Resource):
    """A class representing the analysis response on call /analysis."""

    vector_databases: tuple = build_vector_database()
    apt_descriptions: dict = retrieve_apt_descriptions()

    def post(self):
        """Handle a given get request, forward it to the llm and give the response back.

        Return:
            dict: response in json.
            int: code.

        """
        try:
            parser: RequestParser = RequestParser()
            parser.add_argument("prompt", type=str, required=True)
            args = parser.parse_args(strict=True)

            prompt: str = args["prompt"]
            response: str = send_prompt(prompt, self.vector_databases, self.apt_descriptions)

            defined_json = SchemaParser()

            statistics = defined_json.correct_structure(llama_json_parser(response))
            return {
                "message": "success",
                "response": response,
                "data_points": statistics,
            }, 200
        except ResponseError:
            return {"message": "LLM_error"}, 500
        except ConnectTimeout:
            return {"message": "LLM_error"}, 500
