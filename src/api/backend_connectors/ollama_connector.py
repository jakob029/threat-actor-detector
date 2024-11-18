"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str

"""

import os
from ollama import Client


def send_prompt(prompt: str | list) -> str:
    """Send prompt to llm.

    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | list): the prompt to send.

    Return:
        llm_response (str): The response of the LLM.

    """
    llm_model = os.environ.get("LLM_MODEL", default="llama3.2")
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
    llm_preprompt_path = os.environ.get("LLM_PREPROMPT_PATH", default="./prepromt")

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    with open(llm_preprompt_path, "r") as f:
        preprompt = f.read()
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    # send prompt
    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)

    return llm_response["message"]["content"]
