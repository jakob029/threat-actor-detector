"""User endpoints.

Classes:
    Authentication

"""
from flask_restful import Resource


class Authentication(Resource):
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
