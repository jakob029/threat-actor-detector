"""Main API file."""

from flask import Flask
from flask_restful import Api
from endpoints.ollama_endpoint import Analyzis
import logging

logging.basicConfig(format="[ %(asctime)s ] %(message)s", datefmt="%m/%d/%Y %H:%M:%S")

app = Flask(__name__)
api = Api(app)

api.add_resource(Analyzis, "/analyzis", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
