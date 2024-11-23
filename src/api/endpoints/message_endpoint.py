"""Handle message actions.

Class:
    MessageEndpoint

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from backend_connectors.database_connector import get_messages, reset_conversation
from api_exceptions import DatabaseException
from handlers.conversation_handler import hold_conversation

logger = logging.getLogger(__name__)


class MessagesEndpoint(Resource):
    """Class representing messages endpoint."""

    def get(self, cid):
        """Return conversation messages.

        Arguments:
            cid (str): conversation id.

        Returns:
            response (dict): list of messages.

        """
        messages = get_messages(cid)

        for message in messages.copy():
            if message["role"] == "system":
                messages.remove(message)

        return {"message": "success", "conversation_history": messages}, 200

    def post(self):
        """Add message.

        Returns:
            response (dict): response

        """
        try:
            parser: RequestParser = RequestParser()
            parser.add_argument("text", type=str, required=True)
            parser.add_argument("cid", type=str, required=True)
            args = parser.parse_args(strict=True)

            response = hold_conversation(args["cid"], args["text"])

            return {"messgae": "success", "response": response}, 200
        except DatabaseException as e:
            return {"message": e.message}, 200
        except Exception:
            return {"message": "something went wrong."}, 500

    def delete(self, cid: str):
        """Reset conversation.

        Returns:
            response (dict): response

        """
        try:
            reset_conversation(cid)

            return {"messgae": "success"}, 200

        except DatabaseException as e:
            return {"message": e.message}, 200
        except Exception:
            return {"message": "something went wrong."}, 500
