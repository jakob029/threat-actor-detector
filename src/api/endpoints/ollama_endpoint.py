"""Ollama requests.

Classes:
    Analyzis
"""

import logging

from httpx import ConnectTimeout
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from ollama import ResponseError
from src.api.backend_connectors.database_connector import get_graph, add_message, reset_conversation
from src.api.backend_connectors.ollama_connector import construct_analyze_prompt
from src.api.backend_connectors.ollama_connector import send_analyze_prompt
from src.api.handlers.statistic_parser import llama_json_parser
from src.api.handlers.statistic_json_parser import SchemaParser
from src.api.handlers.conversation_handler import set_graph_to_conversation

from src.api.api_exceptions import UNKNOWN_ISSUE, DatabaseException


logger = logging.getLogger(__name__)


class Analyzis(Resource):
    """A class representing the analysis response on call /analysis."""

    def get(self, cid: str):
        """Get data points and return them.

        Arguments:
            cid (str): conversation id.

        """
        try:
            data_points = get_graph(cid)
        except DatabaseException as e:
            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except Exception as e:
            logger.error(e)
            return {"message": "Something went wrong."}, 500

        return {"message": "success", "data_points": data_points}, 200

    def post(self):
        """Handle a given get request, forward it to the llm and give the response back.

        Return:
            dict: response in json.
            int: code.

        """
        parser: RequestParser = RequestParser()
        parser.add_argument("prompt", type=str, required=True)
        parser.add_argument("cid", type=str, required=True)
        args = parser.parse_args(strict=True)

        prompt: str = args["prompt"]
        cid: str = args["cid"]
        counter: int = 0

        constucted_prompt: list = construct_analyze_prompt(prompt, cid)
        while True:
            try:
                response: str = send_analyze_prompt(constucted_prompt)
                defined_json = SchemaParser()
                statistics = defined_json.correct_structure(llama_json_parser(response))

                set_graph_to_conversation(cid, statistics)
                add_message(response, "assistant", cid)

            except ResponseError as e:
                logger.error(str(e))
                if counter < 3:
                    reset_conversation(cid)
                    continue

                return {"message": "success", "response": response}, 200
            except ConnectTimeout:
                return {"message": "LLM_error"}, 500
            except TypeError:
                return {"message": "parse error"}, 500
            except DatabaseException as e:
                if e.code == UNKNOWN_ISSUE:
                    return {"message": e.message}, 500
                return {"message": e.message}, 200
            except Exception as e:
                if counter < 3:
                    reset_conversation(cid)
                    continue

                logger.error(e)
                return {"message": "success", "response": response}, 200

            return {
                "message": "success",
                "response": response,
                "data_points": statistics,
            }, 200
