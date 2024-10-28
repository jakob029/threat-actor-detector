"""Main API file."""

from flask import Flask
from flask_restful import Api
from endpoints import Registration, Analyzis
import logging

logging.basicConfig(
    format="[ %(asctime)s ] %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG
)

app = Flask(__name__)
api = Api(app)

api.add_resource(Analyzis, "/analyzis", methods=["POST"])
api.add_resource(Registration, "/user/register", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
