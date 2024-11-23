"""Module handling all conversation related tasks."""

from backend_connectors.database_connector import get_messages, add_message, add_graph_point
from backend_connectors.ollama_connector import send_prompt
from ollama import ResponseError


def hold_conversation(cid: str, message: str) -> str:
    """Send message to llm and return the response.

    It gets the previous conversation history adds the new message and sends
    it to the llm. The response is saved in the database and sent baack to
    the client.

    Arguments:
        cid (str): Conversation id.
        message (str): User message.

    Returns:
        response (str): LLM response.

    Raises:
        DatabaseException

    """
    # Save new message to database.
    add_message(message, "user", cid)

    # Get conversation history.
    messages: list = get_messages(cid)

    # TODO: add vector db preprompting.
    if len(messages) == 0:
        pass

    messages += [{"role": "user", "content": message}]

    # send prompt and save the response.
    response = send_prompt(messages)
    add_message(response, "assistant", cid)

    return response


def set_graph_to_conversation(cid: str, points: dict) -> None:
    """Sets the graph for the conversation.

    Arguments:
        cid (str): conversation id.
        points (dict): graph points.

    Raises:
        DatabaseException
        TypeError
        ResponseError

    """
    if len(points) < 1:
        raise ResponseError("Empty data points.")

    for key, value in points.items():
        if not isinstance(key, str):
            raise TypeError("Expected string.")

        add_graph_point(cid, key, int(value))
