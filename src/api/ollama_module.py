from flask_restful import Resource, reqparse
from ollama import Client

from config import read_config


class Analysis(Resource):
    def get(self):
        config = read_config()

        if config is None:
            return {'status': 'error', 'message': 'Configuration file does not exist.'}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('question', type=str, required=True)
        args = parser.parse_args(strict=True)
        question = args['question']

        client = Client(host=config.llm_address)
        llm_response = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': question
            }
        ])



        return {"resp": llm_response}, 200


class Test(Resource):
    def get(self):
        config = read_config()
        if config is None:
            return {'status': 'error', 'message': 'Configuration file does not exist.'}, 400

        client = Client(host=config.llm_address)
        llm_response = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': 'what is a rock?'
            }
        ])

        # Testing llm chat.
        resp = llm_response["message"]["content"]
        print(resp)
        llm_response = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': 'what is a rock?'
            }, {
                'role': 'assistant',
                'content': resp
            }, {
                'role': 'user',
                'content': 'can you write a song about it?'
            }
        ])
        return {'llm-response': llm_response['message']}, 200
        


