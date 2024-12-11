"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str

"""

import os
import logging
from pathlib import Path

import requests
from ollama import Client
from src.api.backend_connectors.database_connector import add_message


logger = logging.getLogger(__name__)


def send_prompt(prompt: list) -> str:
    """Send basic proompt to llm.

    Arguments:
        prompt (list): prompt to send, with previous history.

    Returns:
        response (str): llm response.

    """
    llm_model = os.environ.get("LLM_MODEL", default="llama3.1")
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")

    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)

    return llm_response["message"]["content"]


def send_analyze_prompt(prompt: str | list, cid: str) -> str:
    """Send prompt to llm.

    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | list): the prompt to send.
        cid (str): Conversation id.

    Return:
        llm_response (str): The response of the LLM.

    """
    location = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    llm_model = os.environ.get("LLM_MODEL", default="llama3.1")
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
    llm_preprompt_path = os.environ.get("LLM_PREPROMPT_PATH", default=f"{location}/prepromt")

    vector_db_host = os.environ.get("VECTOR_DB_HOST", default="http://100.77.88.70")
    vector_db_port = os.environ.get("VECTOR_DB_PORT", default="5000")

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    skip_vector_database: bool = False
    logger.warning(vector_db_host)
    try:
        vector_db_prompt = {"prompt": prompt[0]["content"]}
    except KeyError:
        logger.warning("Skipping vector DB connection.")
        skip_vector_database = True

    if not skip_vector_database:
        try:
            vector_database_response = requests.get(
                f"http://{vector_db_host}:{vector_db_port}/GroupAnalyzer",
                json=vector_db_prompt,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        except requests.exceptions.ConnectTimeout:
            logger.warning("Not able to connect to vector database.")

        prompt.insert(
            0,
            {
                "role": "system",
                "name": "Vector database",
                "content": f"The vector database analyzed this: {vector_database_response}",
            },
        )

    if not skip_vector_database:
        group_names = vector_database_response.json()["response"]["ids"][0]

        describer_payload = ":".join(group_names)
        descriptor_prompt = {"groups": describer_payload}
        description_response = requests.post(
            f"http://{vector_db_host}:{vector_db_port}/GroupDescriptor",
            json=descriptor_prompt,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        prompt.insert(
            0,
            {
                "role": "system",
                "name": "Database",
                "content": f"Description for sourced groups: {description_response.json()['descriptor']}",
            },
        )

    with open(llm_preprompt_path, "r", encoding="utf-8") as f:
        preprompt = f.read()
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    for prompt_i in prompt:
        add_message(prompt_i["content"], prompt_i["role"], cid)

    client: Client = Client(host=llm_address, timeout=120)
    response = client.chat(model=llm_model, messages=prompt)["message"]["content"]

    return response
