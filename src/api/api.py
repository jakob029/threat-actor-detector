"""
Main API file.
"""

from flask import Flask
from flask_restful import Api
from ollama_module import Analysis, Test


app = Flask(__name__)
api = Api(app)

api.add_resource(Test, "/test")
api.add_resource(Analysis, "/analysis")

if __name__ == "__main__":
    app.run(debug=True)
