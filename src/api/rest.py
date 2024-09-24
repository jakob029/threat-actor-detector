from flask import Flask
from flask_restful import Resource, Api
import logging
from datetime import date



from ollama_connector import test

logging.basicConfig(filename=f"logs/api-{date.today()}.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

class HelloLlama(Resource):
    def get(self, question):
        return test(question)


class HelloWorld(Resource):
    def get(self):
        return {"Hello": "hej"}


api.add_resource(HelloWorld, '/')
api.add_resource(HelloLlama, '/<string:question>')

if __name__ == "__main__":
    app.run(debug=True)
