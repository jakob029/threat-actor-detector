<<<<<<< HEAD
"""User end points.

Classes:
    Authentication
    Registration

"""

import logging
=======
"""User endpoints.

Classes:
    Authentication

"""
>>>>>>> c80bb9db3d3088714847d20867e2008e8a727d29
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from handlers import register, authenicate
from api_exceptions import AuthenticationException, RegistrationException

logger = logging.getLogger(__name__)


class Authentication(Resource):
<<<<<<< HEAD
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

        return {"message": "User registered"}, 200
=======
    """Class representing an suthentication response."""

    def get(self, id: str):
        """Get user info.

        Arguments:
            id (str): user id

        """
        return {}, 200

    def post(self, password: str, username: str):
        """Sign user in.

        Arguments:
            password (str): user password hash.
            username (str): user name.

        """
        return {}, 200
>>>>>>> c80bb9db3d3088714847d20867e2008e8a727d29
