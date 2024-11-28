"""Group descriptor endpoint for vector db API."""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from build_dataset.run import retrieve_apt_descriptions


class GroupDescriptor(Resource):
    """Group descriptor endpoint for vector db API."""

    apt_descriptions: dict = retrieve_apt_descriptions()

    def post(self) -> tuple:
        """Retrieve descriptions for given APT groups.

        Args:
        ----
            groups: Given groups separated by ':'.

        Returns:
        -------
            Descriptions for each given group together with the group name.
        """
        parser: RequestParser = RequestParser()
        parser.add_argument("groups", type=str, required=True)
        args = parser.parse_args(strict=True)

        full_group_descriptor = retrieve_apt_descriptions()

        groups = args["groups"].split(":")

        group_descriptor = {group: full_group_descriptor[group] for group in groups}

        return {"descriptor": group_descriptor}, 200
