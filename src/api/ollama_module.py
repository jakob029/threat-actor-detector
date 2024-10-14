from flask_restful import Resource, reqparse
from ollama import Client

class Test(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question', type=str, required=True)
        args = parser.parse_args(strict=True)
        question = args['question']
        client = Client(host='http://100.77.88.10')
        llm_response = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': question
            }
        ])

        return {'llm-response': llm_response}, 200
        


