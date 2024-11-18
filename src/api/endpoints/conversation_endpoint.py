"""Conversation requests"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

logger = logging.getLogger(__name__)

class Conversation(Resource):
    """Class handling all conversation requests."""

    def get(self, uid: str):
        pass


    def post(self):
        pass
