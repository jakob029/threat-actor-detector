"""Handle message actions.

Class:
    MessageEndpoint

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from backend_connectors.database_connector import get_messages, reset_conversation
from api_exceptions import DatabaseException, CONVERSATION_DOES_NOT_EXIST
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
        try:
            messages = get_messages(cid)

            for message in messages.copy():
                if message["role"] == "system":
                    messages.remove(message)
        except DatabaseException as e:
            logger.error(e.message)
            return {"message": "something went wrong."}, 500
        except Exception as e:
            logger.error(e)
            return {"message": "something went wrong."}, 500
        else:
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

        except DatabaseException as e:
            if e.code == CONVERSATION_DOES_NOT_EXIST:
                return {"message": e.message}, 200

            logger.error(e.message)
            return {"message": "something went wrong."}, 500
        except Exception as e:
            logger.error(e)
            return {"message": "something went wrong."}, 500
        else:
            return {"messgae": "success", "response": response}, 200

    def delete(self, cid: str):
        """Reset conversation.

        Returns:
            response (dict): response

        """
        try:
            reset_conversation(cid)

        except DatabaseException as e:
            if e.code == CONVERSATION_DOES_NOT_EXIST:
                return {"message": e.message}, 200

            logger.error(e.message)
            return {"message": "something went wrong."}, 500
        except Exception as e:
            logger.error(e)
            return {"message": "something went wrong."}, 500
        else:
            return {"messgae": "success"}, 200
