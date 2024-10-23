"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str
"""

from collections.abc import Sequence
from config_handler import Config, read_config
from ollama import Client, Message


def send_prompt(prompt: str | Sequence[Message]) -> str:
    """Send a prompt to the llm and return it.

    Can use chat history by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | Sequence[Message]): the prompt to send.

    Return:
        llm_response (str): The response of the LLM.

    """
    config: Config = read_config()

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": "prompt"}]

    # send prompt
    client: Client = Client(host=config.llm_address)
    print(config.llm_address)
    llm_response = client.chat(model=config.llm_model, messages=prompt)

    return llm_response["response"]
