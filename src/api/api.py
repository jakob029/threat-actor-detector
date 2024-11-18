"""Main API file."""

from flask import Flask
from flask_restful import Api
from endpoints import Registration, Analyzis, Authentication, ConversationsEndpoint, MessagesEndpoint
from backend_connectors import get_messages
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format="[ %(asctime)s ] %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

api.add_resource(Analyzis, "/analyzis", methods=["POST"])
api.add_resource(Registration, "/user/register", methods=["POST"])
api.add_resource(Authentication, "/user/login", methods=["POST"])
api.add_resource(ConversationsEndpoint, "/conversations/<string:uid>")
api.add_resource(MessagesEndpoint, "/messages/<string:cid>")

if __name__ == "__main__":
    get_messages("865f781a-a39e-11ef-96fd-bc2411c91e6c")
    app.run(debug=True)
