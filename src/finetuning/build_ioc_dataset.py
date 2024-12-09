"""Construct a dataset of IoCs to finetune the llm."""

import os
import json

from ollama import Client
import mysql.connector

LLM_IP_ADDRESS = "100.77.88.10"

DATABASE_IP_ADDRESS: str = "100.77.88.30"
MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE: str = "ioc_apt_mapping"
MYSQL_USER: str = "remote_user"


PREPROMPT = (
    "I am creating a dataset used for training an llm. Please insert this random string into a random sentence: "
)


def generate_dataset():
    """Generate a dataset for IoC with the format {"IoC": "IoC in sentence"}."""
    indicators = _source_iocs()
    dataset = _itteartive_dataset_creater(indicators[0:100] + indicators[300:400])

    with open("ioc_dataset.json", "w", encoding="utf-8") as file:
        json.dump(dataset, file)


def _source_iocs() -> list:
    """Source iocs form the database.

    Returns:
        Returns a list of tuples for row entries in the database.
    """
    connection = mysql.connector.connect(
        host=DATABASE_IP_ADDRESS, database=MYSQL_DATABASE, user=MYSQL_USER, password=MYSQL_PASSWORD
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ioc_table")

    result = cursor.fetchall()

    return result


def _itteartive_dataset_creater(iocs: tuple | list) -> dict:
    """Itterativly create the dataset for each ioc.

    Args:
        iocs: A list of a bunch of IoCs contained on index 0 in a tuple.
    """
    training_set = {}

    for count, ioc in enumerate(iocs):
        ioc_specification = ioc[0]
        sentence = _send_creation_prompt(PREPROMPT + ioc_specification)
        training_set[ioc_specification] = sentence
        if count % 100 == 0:
            print(f"{count/len(iocs)}% complete")

    return training_set


def _send_creation_prompt(prompt: str) -> str:
    """Send proompt to llm focused on creating a datset entry.

    Arguments:
        prompt: prompt to send, with previous history.

    Returns:
        response: llm response.
    """
    prompt = [{"role": "user", "content": prompt}]
    llm_model = os.environ.get("LLM_MODEL", default="llama3.2")
    llm_address = os.environ.get("LLM_ADDRESS", default=LLM_IP_ADDRESS)

    client: Client = Client(host=llm_address, timeout=120)
    llm_response = client.chat(model=llm_model, messages=prompt)

    return llm_response["message"]["content"]
