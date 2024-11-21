"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str

"""

import os
from pathlib import Path

from ollama import Client


def send_prompt(prompt: str | list, vector_databases: tuple | None = None, descriptor: dict | None = None) -> str:
    """Send prompt to llm.

    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | list): the prompt to send.
        vector_databases: Tuple of VectorDB instances.
        descriptor: Group description dict.

    Return:
        llm_response (str): The response of the LLM.

    """
    location = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    llm_model = os.environ.get("LLM_MODEL", default="llama3.2")
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
    llm_preprompt_path = os.environ.get("LLM_PREPROMPT_PATH", default=f"{location}/prepromt")

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    if vector_databases:
        (description_builder,) = vector_databases
        relation_response = description_builder.collection.query(
            query_texts=prompt[0]["content"], n_results=10, include=["distances"]
        )
        prompt.insert(
            0,
            {
                "role": "system",
                "name": "Vector database",
                "content": f"The vector database analyzed this: {relation_response}",
            },
        )

    if descriptor:
        group_descriptor = {group: descriptor.get(group) for group in relation_response}

        prompt.insert(
            0,
            {
                "role": "system",
                "name": "Database",
                "content": f"Description for sourced groups: {group_descriptor}",
            },
        )

    with open(llm_preprompt_path, "r") as f:
        preprompt = f.read()
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    # send prompt
    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)

    return llm_response["message"]["content"]
