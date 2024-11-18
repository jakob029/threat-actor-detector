"""Handle message actions

Class:
    MessageEndpoint

"""

import logging
from flask_restful import Resource
from backend_connectors import get_messages


logger = logging.getLogger(__name__)


class MessagesEndpoint(Resource):
    """Class representing messages endpoint"""

    def get(self, cid):
        """Return conversation messages.

        Arguments:
            cid (str): conversation id.

        Returns:
            response (dict): list of messages.

        """
        messages = get_messages(cid)
        return {"message": "success", "conversation_history": messages}, 200
