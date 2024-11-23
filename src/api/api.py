"""Main API file."""

from flask import Flask
from flask_restful import Api
from endpoints.user_endpoint import Registration, Authentication
from endpoints.ollama_endpoint import Analyzis
from endpoints.message_endpoint import MessagesEndpoint
from endpoints.conversation_endpoint import ConversationsEndpoint
import logging
from dotenv import load_dotenv

# logging settings
logging.basicConfig(format="[ %(asctime)s ] %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)

load_dotenv()

# load env
logging.info("loaded .env")
load_dotenv()

app = Flask(__name__)
api = Api(app)

api.add_resource(Analyzis, "/analyzis/<string:cid>", "/analyzis", methods=["GET", "POST"])
api.add_resource(Registration, "/user/register", methods=["POST"])
api.add_resource(Authentication, "/user/login", methods=["POST"])
api.add_resource(ConversationsEndpoint, "/conversations/<string:uid>", "/conversations", methods=["GET", "POST"])
api.add_resource(MessagesEndpoint, "/messages/<string:cid>", "/messages", methods=["GET", "DELETE", "POST"])

if __name__ == "__main__":
    app.run(host="100.77.88.40")
