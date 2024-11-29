"""Group analyzer endpoint for vector db API."""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from build_dataset.run import build_vector_database


class GroupAnalyzer(Resource):
    """Group analyzer endpoint for vector db API."""

    vector_databases: tuple = build_vector_database()

    def get(self) -> tuple:
        """Retrieve a response from the vector database.

        Args:
        ----
            prompt: Prompt used to prompt the vector database.

        Returns:
        -------
            Response given from the vector database including 'ids' for
            represented by names of APT groups & distances to those ids.
        """
        parser: RequestParser = RequestParser()
        parser.add_argument("prompt", type=str, required=True)
        args = parser.parse_args(strict=True)

        (description_builder,) = self.vector_databases

        relation_response = description_builder.collection.query(
            query_texts=args["prompt"], n_results=10, include=["distances"]
        )

        return {"response": relation_response}, 200
