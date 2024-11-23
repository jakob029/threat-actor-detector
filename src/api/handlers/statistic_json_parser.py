"""Parser for LLM written JSON likelihood estimations."""

from jsonschema import validate, ValidationError


class SchemaParser:
    """Parser for LLM written JSON likelihood estimations."""

    ANALYSIS: bool

    name_struct: tuple = ("name", "Name", "Names", "names")
    likelihood_estimate: tuple = ("Likelihood", "likelihood", "Likelihoods", "likelihoods")

    @property
    def default_structure(self) -> dict:
        """Default defined structure with integer or floating point number estimators."""
        return {"type": "object", "patternProperties": {r"[a-zA-Z0-9._ ]+": {"type": "number"}}}

    @property
    def default_string_structure(self) -> dict:
        """Default defined structure with string point number estimators."""
        return {"type": "object", "patternProperties": {r"[a-zA-Z0-9._ ]+": {"type": "string"}}}

    def correct_structure(self, structure) -> dict:
        """Get a structure dictionary with defined likelihood estimation.

        Args:
            structure: The unstructured dictionary.
        """
        self.ANALYSIS = False

        validate_structures = (self._default_test, self._default_string_test)
        for validator in validate_structures:
            if validator(structure):
                return self._correct_intangers(structure)

        structure = self._one_base_structure(structure)
        if self.ANALYSIS and self._accepted_result(structure):
            return self._correct_intangers(structure)

        structure = self._multilayer_dict(structure)
        if self.ANALYSIS and self._accepted_result(structure):
            return self._correct_intangers(structure)

        return {}

    @staticmethod
    def _correct_intangers(structure: dict) -> dict:
        """Convert potential float values to intages.

        Args:
            structure: The unstructured dictionary.
        """
        if isinstance(structure.values()[0], int):
            return structure

        if isinstance(structure.values()[0], float):
            return {group: int(value * 100) for group, value in structure.items()}

        return structure

    def _accepted_result(self, structure) -> bool:
        """Confirmation that the structure is accepted.

        Args:
            structure: The unstructured dictionary.
        """
        return self._default_test(structure) | self._default_string_test(structure)

    def _default_test(self, structure) -> bool:
        """Default structure confirmation.

        Args:
            structure: The unstructured dictionary.
        """
        try:
            validate(instance=structure, schema=self.default_structure)
            return True
        except ValidationError:
            return False

    def _default_string_test(self, structure) -> bool:
        """Default structure with string value estimation confirmation.

        Args:
            structure: The unstructured dictionary.
        """
        try:
            validate(instance=structure, schema=self.default_string_structure)
            return True
        except ValidationError:
            return False

    def _one_base_structure(self, structure) -> dict:
        """Reorientate dictionary with random base key and possible other redundant keys.

        Args:
            structure: The unstructured dictionary.
        """
        if len(structure) != 1:
            return structure

        structure = structure[next(iter(structure))]
        if isinstance(structure, dict):
            return structure

        complete_dict = {}
        if isinstance(structure, list):
            group_decor = [key for key in structure[0].keys() if key in self.name_struct]
            estimate_decor = [key for key in structure[0].keys() if key in self.likelihood_estimate]
            if not group_decor or not estimate_decor:
                return {}

            for instance in structure:
                complete_dict[instance[group_decor[0]]] = instance[estimate_decor[0]]

        self.ANALYSIS = True
        return complete_dict

    def _multilayer_dict(self, structure):
        """Reorientate nestled dictionary to flat defined format, removal of redundant keys.

        Args:
            structure: The unstructured dictionary.
        """
        try:
            estimate_decor = [key for key in structure[next(iter(structure))].keys() if key in self.likelihood_estimate]
        except AttributeError:
            return {}

        complete_dict = {}
        for instance in structure:
            complete_dict[instance] = structure[instance].get(estimate_decor[0])

        self.ANALYSIS = True
        return complete_dict
