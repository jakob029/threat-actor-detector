"""Collection of all the llm requests and functions.

Functions:
    send_prompt(prompt) -> str

"""

import os
import logging
from pathlib import Path
import copy
import requests

from ollama import Client
from src.api.backend_connectors.database_connector import add_message
from src.api.backend_connectors.database_connector import collect_ioc_mapping


logger = logging.getLogger(__name__)


def _guardrail(llm_response: str, client: Client, llm_model: str = "llama3.1") -> bool:
    """Guardrail for the output prompt that checks for offensive content.

    Args:
        llm_response: Any generated response from an llm.
        client: An ollama client.
        llm_model (optional): Model to use for guardrail.

    Response:
        True if guardrail is broken, otherwise False.
    """
    guardrail_prompt = (
        "You are now acting as a guardrail, trying to prevent output that could be considered offensive."
        " Respond with only yes or no, could the following message be considered offensive?"
    )
    text_prompt = guardrail_prompt + llm_response

    prompt = [{"role": "user", "content": text_prompt}]
    guardrail_response = client.chat(model=llm_model, messages=prompt)
    guardrail_response_text = guardrail_response["message"]["content"]

    if "yes" == guardrail_response_text:
        return True

    return False


def send_prompt(prompt: list) -> str:
    """Send basic proompt to llm.

    Arguments:
        prompt (list): prompt to send, with previous history.

    Returns:
        response (str): llm response.

    """
    llm_model = os.environ.get("LLM_MODEL", default="llama3.1")
    llm_address = os.environ.get("LLM_ADDRESS", default="https://llm.infra.encryptedallies.com")

    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)
    llm_response_text = llm_response["message"]["content"]

    if _guardrail(llm_response_text, client):
        return "Return prompt violated guardrail."

    return llm_response_text


def construct_analyze_prompt(prompt: str | list, cid: str) -> tuple:
    """Send prompt to llm.

    Send a prompt to the llm and return it. Can use chat history
    by having prompt be a Sequence[Message] type.

    Arguments:
        prompt (str | list): the prompt to send.
        cid (str): Conversation id.

    Return:
        Tuple with format (PROMPT_FOR_LLM, IOC_FLAG) where the IoC flag
        specifies if an IoC was mapped.
    """
    location = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    llm_address = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
    llm_preprompt_path = os.environ.get("LLM_PREPROMPT_PATH", default=f"{location}/prepromt")

    vector_db_host = os.environ.get("VECTOR_DB_HOST", default="100.77.88.70")
    vector_db_port = os.environ.get("VECTOR_DB_PORT", default="5000")

    ioc_parser_model = "ioc_parser"

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    ioc_select_prompt = copy.deepcopy(prompt)

    skip_vector_database: bool = False

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
                "content": f"Vector distance (not procentages): {vector_database_response.json()}",
            },
        )

    if not skip_vector_database:
        logger.info(f"The Vector_db response: {vector_database_response.json()}")

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

    client: Client = Client(host=llm_address, timeout=120)
    IOC_FLAG: bool = False

    select_ioc_prompt: str = "Could you select the IoC in this sentence, and respond only with the IoC: "
    for _ in range(5):
        ioc_select_prompt[0]["content"] = select_ioc_prompt + ioc_select_prompt[0]["content"]

        selected_ioc = client.chat(model=ioc_parser_model, messages=ioc_select_prompt)["message"]["content"]
        logger.info(f"Running {ioc_parser_model}")
        logger.info(f"The IOC model found: {selected_ioc}")
        ioc_info = collect_ioc_mapping(selected_ioc)
        if ioc_info:
            break

    if ioc_info:
        IOC_FLAG = True
        prompt.insert(
            -2,
            {
                "role": "system",
                "name": "IoC database",
                "content": f"The IoC {selected_ioc} is related to {ioc_info[1]} according to the database.",
            },
        )

    with open(llm_preprompt_path, "r", encoding="utf-8") as f:
        preprompt = f.read()
        prompt.insert(0, {"role": "system", "name": "Threat Analyzer", "content": preprompt})

    for prompt_i in prompt:
        add_message(prompt_i["content"], prompt_i["role"], cid)

    logger.info(f"The final llm prompt was: |{prompt}|")

    return prompt, IOC_FLAG
