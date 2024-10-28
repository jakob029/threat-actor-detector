import logging
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from handlers import register

logger = logging.getLogger(__name__)

class Authentication(Resource):
    def get(self):
        return {}, 200

    def post(self):
        return {}, 200


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
