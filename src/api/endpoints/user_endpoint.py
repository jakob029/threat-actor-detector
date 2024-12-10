"""User end points.

Classes:
    Authentication
    Registration

"""

import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from argon2.exceptions import VerifyMismatchError
from src.api.handlers.user_handler import register, authenicate, validate_user_delition
from src.api.api_exceptions import (
    DELETETION_ERROR,
    PASSWORD_TOO_WEAK,
    UNKNOWN_ISSUE,
    USER_ALREADY_EXIST,
    USER_DOES_NOT_EXIST,
    USERNAME_TOO_LONG,
    VARIABLE_NOT_SET,
    AuthenticationException,
    DatabaseException,
    RegistrationException,
)

logger = logging.getLogger(__name__)


class Authentication(Resource):
    """Class representing authentications."""

    def delete(self, uid: str):
        """Deletes the user."""
        parser: RequestParser = RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)

        args = parser.parse_args(strict=True)

        try:
            validate_user_delition(uid, args["password"], args["username"])
        except AuthenticationException as e:
            if e.code in (USERNAME_TOO_LONG, USER_DOES_NOT_EXIST):
                return {"message": "Password or User is wrong."}, 200

            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except DatabaseException as e:
            if e.code in (VARIABLE_NOT_SET, UNKNOWN_ISSUE):
                logger.error(e.message)
                return {"message": "Something went wrong."}, 200

            if e.code == USER_DOES_NOT_EXIST:
                return {"message": "User does not exist."}, 200
            
            if e.code == DELETETION_ERROR:
                return {"message": e.message}, 200

            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except VerifyMismatchError:
            return {"message": "Password or User is wrong."}
        except Exception as e:
            logger.error(e)
            return {"message": "Something went wrong"}, 500


        return {"message": "success"}, 200


    def post(self):
        """Sign in the new user."""
        parser: RequestParser = RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)

        args = parser.parse_args(strict=True)

        try:
            uid: str = authenicate(args["username"], args["password"])

        except AuthenticationException as e:
            if e.code in (USERNAME_TOO_LONG, USER_DOES_NOT_EXIST):
                return {"message": "Password or User is wrong."}, 200

            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except DatabaseException as e:
            if e.code in (VARIABLE_NOT_SET, UNKNOWN_ISSUE):
                logger.error(e.message)
                return {"message": "Something went wrong."}, 200

            if e.code == USER_DOES_NOT_EXIST:
                return {"message": "User does not exist."}, 200

            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except VerifyMismatchError:
            return {"message": "Password or User is wrong."}
        except Exception as e:
            logger.error(e)
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
            if e.code in (PASSWORD_TOO_WEAK, USERNAME_TOO_LONG, USER_ALREADY_EXIST):
                return {"message": e.message}, 200

            logger.error(e.message)
            return {"message": "Something went wrong."}, 500
        except DatabaseException as e:
            logger.error(e)
            return {"message": "Something went wrong."}, 500
        except Exception as e:
            logger.error(e)
            return {"message": "Something went wrong."}, 500

        return {"message": "success"}, 200
