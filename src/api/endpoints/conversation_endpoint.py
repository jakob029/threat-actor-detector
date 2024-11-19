"""Handle Conversation acctions.

Classes:
    ConversationsEndpoint

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from backend_connectors import get_conversations, create_conversation
from api_exceptions import DatabaseException


logger = logging.getLogger(__name__)


class ConversationsEndpoint(Resource):
    """Class representing conversation endpoints."""

    def get(self, uid):
        """Return user conversations.

        Arguments:
            uid (str): user id

        Returns:
            response (dict): resposne

        """
        conversations = get_conversations(uid)
        return {"message": "success", "conversations": conversations}, 200

    def post(self):
        """Create conversation.

        Returns:
            response (dict): response

        """
        try:
            parser: RequestParser = RequestParser()
            parser.add_argument("title", type=str, required=True)
            parser.add_argument("uid", type=str, required=True)

            args = parser.parse_args(strict=True)

            cid = create_conversation(args["uid"], args["title"])

            return {"messgae": "success", "conversation_id": cid}, 200

        except DatabaseException as e:
            return {"message": e.message}, 200
        except Exception:
            return {"message": "something went wrong."}, 500
