"""JSON structure parsing helpers."""

import re
import json
from functools import reduce


def llama_json_parser(content: str, bit: int = 0) -> dict:
    """Attempt to parse a JSON structure given by llama.

    Args:
        content: The output given by the llm model.
        bit: Current position of iterative reduction/replacement functions.
    """
    json_structure = re.split(r"```", content)
    data: str

    if not bit:
        for text in json_structure:
            if "json" in text:
                data = text
                break
        else:
            return {}
    else:
        data = content

    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        formatting_functions = (reduce_bloat, insert_correct_quotations)
        return llama_json_parser(formatting_functions[bit](data), bit + 1) if bit < len(formatting_functions) else {}


def reduce_bloat(json_structure: str) -> str:
    """Reduce a JSON structure from some bloat :D.

    Args:
        json_structure: A flawed JSON structure.
    """
    return reduce(lambda json_object, reductor: json_object.replace(reductor, ""), ["json", "\n", "  "], json_structure)


def insert_correct_quotations(json_structure: str) -> str:
    """Inserts quotation marks on a JSON structure where they are missing.

    Args:
        json_structure: A flawed JSON structure missing quotation marks.
    """
    insert_index = []
    for index, element in enumerate(json_structure):
        if element == "{" and json_structure[index + 1] != '"':
            insert_index.append(index + 1)
        elif element == ":" and json_structure[index - 1] != '"':
            insert_index.append(index)
        elif element == ":" and not re.findall(r"{|\"", json_structure[index : index + 3]):
            insert_index.append(index + 2)
        elif element == "}" and not re.findall(r"}|\"", json_structure[index - 1 : index]):
            insert_index.append(index)

    for index, element in enumerate(sorted(insert_index)):
        json_structure = json_structure[: element + index] + '"' + json_structure[element + index :]

    return json_structure
