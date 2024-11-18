import logging
from flask_restful import Resource
from backend_connectors import get_conversations


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
        return {"messgae": "stahp"}, 200