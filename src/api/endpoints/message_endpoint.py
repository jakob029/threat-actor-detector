"""Handle message actions.

Class:
    MessageEndpoint

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from backend_connectors import get_messages, add_message
from api_exceptions import DatabaseException
from handlers import hold_conversation

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
