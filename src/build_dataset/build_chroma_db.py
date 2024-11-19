"""Vector data base constructor."""

import json
import chromadb
from chromadb.utils import embedding_functions


class VectorDB:
    """Helper class to construct a vector data base."""

    collection: chromadb.api.models.Collection.Collection
    instruction_set: str | list
    name: str

    def __init__(self, instruction_set: str | list, name: str) -> None:
        """Constructor.

        Args:
            instruction_set: Path to or a constructed instruction set for the data base.
            name: Collection name to set.
        """
        self.instruction_set = instruction_set
        self.name = name

    def build_db(self) -> None:
        """Build a vector database saved to memory."""
        chroma_client = chromadb.Client()
        sentence_transformer = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
        self.collection = chroma_client.create_collection(name=self.name, embedding_function=sentence_transformer)
        self._structure_data()
        self._build_collection()

    def _structure_data(self):
        """Construct the instruction_set as a structured list."""
        if not isinstance(self.instruction_set, str):
            return

        with open(self.instruction_set, "r", encoding="utf-8") as comprised_set:
            self.instruction_set = json.load(comprised_set)

    def _build_collection(self) -> None:
        """Build collection based on instruction_set."""
        keys = []
        values = []
        for entries in self.instruction_set:
            if not entries:
                continue
            for groups, target in entries.items():
                if groups in keys:
                    values[keys.index(groups)] += f", {target}"
                    continue
                keys.append(groups)
                values.append(target)

        self.collection.add(documents=values, ids=keys)

    def save_database(self, path: str) -> None:
        """Save the database to the disk.

        Args:
            path: Path to save the database.
        """
        chromadb.PersistentClient(path=path)
