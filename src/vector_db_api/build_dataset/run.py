"""Vector database builder."""

import os
import logging
import json

from src.vector_db_api.build_dataset import construct_db
from src.vector_db_api.build_dataset.construct_db import LOCATION
from src.vector_db_api.build_dataset.build_chroma_db import VectorDB

logging.basicConfig(level=logging.INFO)

PATH = os.path.dirname(os.path.abspath(__file__))

def build_vector_database() -> None | VectorDB:
    """Vector database builder.

    Returns:
        A complete Vector database instance or None if SKIP_VECTOR_DB enviable is set.
    """
    if os.environ.get("SKIP_VECTOR_DB"):
        return

    construction_instance = construct_db.ConstructDataBase()
    construction_instance.construct_atp_descriptor()
    relationship = "manually_constructed_dataset.json"

    relationship_builder = VectorDB(os.path.join(LOCATION, relationship), "group_desc_db")
    relationship_builder.build_db()

    return relationship_builder


def retrieve_apt_descriptions() -> dict:
    """Retrieve descriptions for all APTs."""
    base_tuple = {}
    with open(os.path.join(LOCATION, "group_descriptor.json"), "r", encoding="utf-8") as file:
        descriptor_list = json.load(file)
        for element in descriptor_list:
            base_tuple.update(element)

    return base_tuple
