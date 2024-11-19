"""Vector database builder."""

import os
import logging

import construct_db
from construct_db import LOCATION
from build_chroma_db import VectorDB

logging.basicConfig(level=logging.INFO)


def build_vector_database():
    """Vector database builder."""
    construction_instance = construct_db.ConstructDataBase()
    apt_descriptor = construction_instance.construct_atp_descriptor()
    relations = construction_instance.retrieve_instruction_set_relationships()

    description_builder = VectorDB(apt_descriptor, "group_desc_db")
    description_builder.build_db()

    relation_builder = VectorDB(relations, "relation_db")
    relation_builder.build_db()

    description_builder.save_database(os.path.join(LOCATION, "description_db"))
    logging.info("Saved description_db to disk")

    relation_builder.save_database(os.path.join(LOCATION, "relationship_db"))
    logging.info("Saved relationship_db to disk")


if __name__ == "__main__":
    build_vector_database()
