from flask import Flask
from flask_restful import Api
from ollama_module import Test
from config import read_config


app = Flask(__name__)
api = Api(app)

api.add_resource(Test, "/")

if __name__ == "__main__":
    app.run(debug=True)
