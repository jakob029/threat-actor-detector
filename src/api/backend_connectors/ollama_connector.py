"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str
"""

from ollama import Client
from backend_connectors import LLM_ADDRESS, LLM_MODEL, LLM_PREPROMPT_PATH


def send_prompt(prompt: str | list) -> str:
    """
    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Parameters:
        prompt (str | Sequence[Message]): the prompt to send.

    Return:
        llm_response (str): The response of the LLM.

    """
    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    with open(LLM_PREPROMPT_PATH, "r") as f:
        preprompt = f.read()
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    print(prompt)

    # send prompt
    client: Client = Client(host=LLM_ADDRESS)
    llm_response = client.chat(model=LLM_MODEL, messages=prompt)

    return llm_response["message"]["content"]
