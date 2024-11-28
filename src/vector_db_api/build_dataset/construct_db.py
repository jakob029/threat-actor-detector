"""Construct a dataset using open source MITRE data."""

import os
import json
import subprocess

LOCATION: str = os.path.dirname(os.path.abspath(__file__))


class ConstructDataBase:
    """Base class to construct structured data for vector database."""

    ERROR: int = 0

    def __init__(self, download_files: bool = False) -> None:
        if not download_files and os.path.isdir(os.path.join(LOCATION, "enterprise-attack")):
            return
        status = subprocess.run([f"{LOCATION}/retrieve_data.sh", LOCATION], check=True)
        self.ERROR = status.returncode

    def retrieve_instruction_set_relationships(self, attack_path: str = "enterprise-attack") -> list:
        """Retrieve each relationship for each instruction-set object.

        Args:
            attack_path: Path to the attack information library.
        Returns:
            Constructed APT-TTPs relationship mapping.
        """
        relationship_map = []
        relationship_files = os.listdir(f"{LOCATION}/{attack_path}/relationship")

        for relation_file in relationship_files:
            with open(
                os.path.join(LOCATION, "enterprise-attack/relationship", relation_file), "r", encoding="utf-8"
            ) as file:
                individual_file = json.load(file)
                intrusion_set = self._source_intrusion_set(individual_file)
                if not intrusion_set:
                    continue
                relation_mapping = self._construct_mappings(self._generate_filepaths(intrusion_set))
                relationship_map.append(relation_mapping)

        with open(os.path.join(LOCATION, "constructed_dataset.json"), "w", encoding="utf-8") as file:
            json.dump(relationship_map, file)

        return relationship_map

    def construct_atp_descriptor(self, attack_path: str = "enterprise-attack") -> list:
        """Construct a mapping for APTs and descriptions.

        Args:
            attack_path: Path to the attack information library.
        Returns:
            Constructed mapped list containing descriptions and APTs.
        """
        apt_map = []
        relationship_files = os.listdir(f"{LOCATION}/{attack_path}/intrusion-set")
        for relation_file in relationship_files:
            with open(
                os.path.join(LOCATION, "enterprise-attack/intrusion-set", relation_file), "r", encoding="utf-8"
            ) as file:
                individual_file = json.load(file)
                intrusion_object = individual_file.get("objects")
                if not intrusion_object:
                    continue
                description = intrusion_object[0].get("description")
                aliases = intrusion_object[0].get("aliases")
                if not aliases:
                    continue
                apt_map.append({alias: description for alias in aliases})

        with open(os.path.join(LOCATION, "group_descriptor.json"), "w", encoding="utf-8") as file:
            json.dump(apt_map, file)

        return apt_map

    @staticmethod
    def _source_intrusion_set(json_data: dict) -> tuple | None:
        """Source intrusion-sets found in relationships.

        Args:
            json_data: Some json structured data containing a relationship.

        Returns:
            If an intrusion-set was found, the correlated relation is returned.
        """
        objects = json_data.get("objects")
        if not objects:
            return None

        if "intrusion-set" not in objects[0].get("source_ref"):
            return

        source = objects[0].get("source_ref")
        target = objects[0].get("target_ref")
        return source, target

    @staticmethod
    def _generate_filepaths(relation: str) -> tuple | None:
        """Generate the filepath for a relationship pair in the enterprise-attack dir.

        Args:
            relation: Name of the file for which an absolute path shall be created.

        Returns:
            Generated filepaths.
        """
        source = os.path.join(LOCATION, "enterprise-attack/intrusion-set", f"{relation[0]}.json")
        file_types = [
            "attack-pattern",
            "campaign",
            "course-of-action",
            "identity",
            "intrusion-set",
            "malware",
            "marking-definition",
            "relationship",
            "tool",
        ]

        for file_type in file_types:
            if file_type in relation[1]:
                return source, os.path.join(LOCATION, f"enterprise-attack/{file_type}", f"{relation[1]}.json")

    @staticmethod
    def _construct_mappings(files: tuple) -> dict | None:
        """Construct mapping between group and attack description for given file relation.

        Args:

            files: Relation between intrusion-set & target.
        """
        aliases = []
        with open(files[0], "r", encoding="utf-8") as intrusion_set:
            json_set = json.load(intrusion_set)
            objects = json_set.get("objects")
            if not objects:
                return None
            aliases = objects[0].get("aliases")

        with open(files[1], "r", encoding="utf-8") as target_file:
            json_target_set = json.load(target_file)
            objects = json_target_set.get("objects")
            description = objects[0].get("description")
            if not description:
                description = ""

        if not aliases:
            return None

        return {alias: description for alias in aliases}
