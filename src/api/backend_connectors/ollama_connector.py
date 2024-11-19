"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str

"""

import os
from pathlib import Path
from ollama import Client

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
print("Current sys.path:")
for path in sys.path:
    print(path)

from src.build_dataset.run import build_vector_database


def send_prompt(prompt: str | list) -> str:
    """Send prompt to llm.

    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | list): the prompt to send.

    Return:
        llm_response (str): The response of the LLM.

    """
    location = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    llm_model = os.environ.get("LLM_MODEL", default="llama3.2")
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
    llm_preprompt_path = os.environ.get("LLM_PREPROMPT_PATH", default=f"{location}/prepromt")

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    description_builder, relation_builder = build_vector_database()

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

    ##Also add the apt descriptor and so on IOC stuff ...
    # This should prob be deterministic:
    # apt_descriptor = relation_builder.collection.query(query_texts=db_prompt,n_results=10)
    print(f"Vector db response: {relation_response}")

    with open(llm_preprompt_path, "r") as f:
        preprompt = f.read()
        preprompt = ""
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    # send prompt
    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)

    return llm_response["message"]["content"]
