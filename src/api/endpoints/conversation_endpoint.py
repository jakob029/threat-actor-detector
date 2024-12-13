"""Handle Conversation acctions.

Classes:
    ConversationsEndpoint

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from src.api.backend_connectors.database_connector import (
    delete_all_conversations,
    delete_conversation,
    get_conversations,
    create_conversation,
)
from src.api.api_exceptions import USER_DOES_NOT_EXIST, DatabaseException


logger = logging.getLogger(__name__)


class ConversationsEndpoint(Resource):
    """Class representing conversation endpoints."""

    def delete(self):
        """Deletes user conversations.

        Arguments:
            cid (str): user id

        Returns:
            response (dict): resposne

        """
        parser: RequestParser = RequestParser()
        parser.add_argument("cid", type=str)
        parser.add_argument("uid", type=str)
        args = parser.parse_args()

        try:
            if args["cid"] is not None:
                delete_conversation(args["cid"])
            elif args["uid"] is not None:
                delete_all_conversations(args["uid"])
            else:
                return {"message": "CID or UID is needed."}, 400
        except DatabaseException as e:
            logger.info(e.message)
            return {"message": "something went wrong."}, 500
        except Exception as e:
            logger.info(e)
            return {"message": "something went wrong."}, 500

        return {"message": "success"}, 200

    def get(self, uid):
        """Return user conversations.

        Arguments:
            uid (str): user id

        Returns:
            response (dict): resposne

        """
        try:
            conversations = get_conversations(uid)
        except DatabaseException as e:
            logger.info(e.message)
            return {"message": "something went wrong."}, 500
        except Exception as e:
            logger.info(e)
            return {"message": "something went wrong."}, 500

        return {"message": "success", "conversations": conversations}, 200

    def post(self):
        """Create conversation.

        Returns:
            response (dict): response

        """
        parser: RequestParser = RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("uid", type=str, required=True)

        args = parser.parse_args(strict=True)

        try:
            cid = create_conversation(args["uid"], args["title"])
        except DatabaseException as e:
            if e.code == USER_DOES_NOT_EXIST:
                return {"message": e.message}, 200

            logger.info(e.message)
            return {"message": e.message}, 500
        except Exception as e:
            logger.info(e)
            return {"message": "something went wrong."}, 500

        return {"messgae": "success", "conversation_id": cid}, 200
