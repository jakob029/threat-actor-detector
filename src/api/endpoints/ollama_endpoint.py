"""Ollama requests.

Classes:
    Analyzis
"""

import logging
from httpx import ConnectTimeout
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from ollama import ResponseError
import random
from backend_connectors import send_prompt


logger = logging.getLogger(__name__)


class Analyzis(Resource):
    """A class representing the analysis response on call /analysis."""

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
            response: str = send_prompt(prompt)

            return {"message": "success", "response": response, "data_points": {"testAPT": random.randint(0, 100), "otherAPT": random.randint(0, 100)}}, 200
        except ResponseError:
            return {"message": "LLM_error"}, 500
        except ConnectTimeout:
            return {"message": "LLM_error"}, 500
