"""Main API file."""

import logging
from pathlib import Path
from datetime import datetime
from os import environ

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from src.api.endpoints.user_endpoint import Registration, Authentication
from src.api.endpoints.ollama_endpoint import Analyzis
from src.api.endpoints.message_endpoint import MessagesEndpoint
from src.api.endpoints.conversation_endpoint import ConversationsEndpoint

Path("logs").mkdir(parents=True, exist_ok=True)

HOST = environ.get("BIND_ADDRESS")

logging.basicConfig(
    filename=f"logs/{datetime.now().strftime('%Y-%m-%d')}",
    format="[ %(asctime)s ] %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
    encoding="utf-8",
)

logger = logging.getLogger(__name__)

# load env
load_dotenv()
logging.info("loaded .env")

app = Flask(__name__)
api = Api(app)

api.add_resource(Analyzis, "/analyzis/<string:cid>", "/analyzis", methods=["GET", "POST"])
api.add_resource(Registration, "/user/register", methods=["POST"])
api.add_resource(Authentication, "/user/login", "/user/<string:uid>", methods=["POST", "DELETE"])
api.add_resource(ConversationsEndpoint, "/conversations/<string:uid>", "/conversations", methods=["GET", "POST"])
api.add_resource(MessagesEndpoint, "/messages/<string:cid>", "/messages", methods=["GET", "DELETE", "POST"])

if __name__ == "__main__":
    app.run(host=HOST)
