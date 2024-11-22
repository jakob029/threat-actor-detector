"""Vector database builder."""

import os
import logging
import json

from src.build_dataset import construct_db
from src.build_dataset.construct_db import LOCATION
from src.build_dataset.build_chroma_db import VectorDB

logging.basicConfig(level=logging.INFO)


def build_vector_database() -> tuple:
    """Vector database builder."""
    construction_instance = construct_db.ConstructDataBase()
    construction_instance.construct_atp_descriptor()
    relationship = construction_instance.retrieve_instruction_set_relationships()

    relationship_builder = VectorDB(relationship, "group_desc_db")
    relationship_builder.build_db()

    return (relationship_builder,)


def retrieve_apt_descriptions() -> dict:
    """Retrieve descriptions for all APTs."""
    base_tuple = {}
    with open(os.path.join(LOCATION, "group_descriptor.json"), "r", encoding="utf-8") as file:
        descriptor_list = json.load(file)
        for element in descriptor_list:
            base_tuple.update(element)

    return base_tuple
