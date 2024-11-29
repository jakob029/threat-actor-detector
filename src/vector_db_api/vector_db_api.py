"""API module for vector db."""

from flask import Flask
from flask_restful import Api
from endpoints.group_analyzer import GroupAnalyzer
from endpoints.group_descriptor import GroupDescriptor


FLASK_IMPORT_NAME: str = __name__


def setup_app() -> Flask:
    """Set upp restful API application."""
    app = Flask(FLASK_IMPORT_NAME)
    api = Api(app)
    api.add_resource(GroupAnalyzer, "/GroupAnalyzer", methods=["GET"])
    api.add_resource(GroupDescriptor, "/GroupDescriptor", methods=["POST"])

    app.run()


if __name__ == "__main__":
    app = setup_app()
    app.run()
