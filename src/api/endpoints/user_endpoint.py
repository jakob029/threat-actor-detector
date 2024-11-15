"""User end points.

Classes:
    Authentication
    Registration

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from handlers import register, authenicate
from api_exceptions import AuthenticationException, RegistrationException

logger = logging.getLogger(__name__)


class Authentication(Resource):
    """Class representing authentications."""

    def get(self):
        """Nothing atm."""
        return {}, 200

    def post(self):
        """Sign in the new user."""
        try:
            parser: RequestParser = RequestParser()
            parser.add_argument("username", type=str, required=True)
            parser.add_argument("password", type=str, required=True)

            args = parser.parse_args(strict=True)

            uid: str = authenicate(args["username"], args["password"])

        except AuthenticationException as e:
            return {"message": e.message}, 200
        except Exception as e:
            logger.debug(e)
            return {"message": "Something went wrong"}, 500

        return {"message": "success", "uid": uid}, 200


class Registration(Resource):
    """Class representing registration."""

    def get(self):
        """Nothing atm."""
        return {}, 200

    def post(self):
        """Register a new user."""
        parser: RequestParser = RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)

        args = parser.parse_args(strict=True)

        try:
            register(args["username"], args["password"])
        except RegistrationException as e:
            return {"message": e.message}, 200

        return {"message": "success"}, 200
