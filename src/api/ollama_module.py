"""
Ollama requests.
"""

from flask_restful import Resource, reqparse
from ollama import Client

from config import read_config


class Analysis(Resource):
    "A class representing the analysis response on call /analysis."
    
    def get(self):
        """
        Handle a given get request, forward it to the llm and give the response back.

        Return:
        dict: response in json format.
        int: code.
        """
        config = read_config()

        if config is None:
            return {"message": "Configuration file does not exist."}, 400

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

        return {
            "created": llm_response["created_at"],
            "content": llm_response["message"]["content"],
            "message": "Success"
        }, 200


class Test(Resource):
    "A class representing the test response on call /test."

    def get(self):
        "Qucik conversation test."
        config = read_config()
        if config is None:
            return {'status': 'error', 'message': 'Configuration file does not exist.'}, 400

        # First request asking what is a rock.
        client = Client(host=config.llm_address)
        llm_response_1 = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': 'what is a rock?'
            }
        ])

        # Second request using the previous response and question to ask if it could
        # make a song about it.
        resp = llm_response_1["message"]["content"]
        print(resp)
        llm_response_2 = client.chat(model='llama3.2', messages=[
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

        # Return the song
        return {"messages": [
            {
                'role': 'user',
                'content': 'what is a rock?'
            }, {
                'role': 'assistant',
                'content': llm_response_1['message']['content']
            }, {
                'role': 'user',
                'content': 'can you write a song about it?'
            }, {
                'role': 'assistant',
                'content': llm_response_2['message']['content']
            }
        ]}, 200
        


