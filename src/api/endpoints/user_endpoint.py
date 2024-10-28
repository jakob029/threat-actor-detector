import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from handlers import register, authenicate
from api_exceptions import AuthenticationException

logger = logging.getLogger(__name__)

class Authentication(Resource):
    def get(self):
        return {}, 200

    def post(self):

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
    def get(self):
        return {}, 200

    def post(self):
        parser: RequestParser = RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)

        args = parser.parse_args(strict=True)

        register(args["username"], args["password"])

        return {"message": "User registered"}, 200
