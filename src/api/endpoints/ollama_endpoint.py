"""Ollama requests.

Classes:
    Analyzis
"""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from backend_connectors.ollama_connector import send_prompt
from api_exceptions import ConfigException
import logging

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

            return {"message": "success", "response": response}, 200
        except ConfigException as e:
            logger.error(e.message)
            return {"message": "An error occured, please check the logs."}, 500
