"""Module handling all conversation related tasks."""
from backend_connectors import get_messages, send_prompt, add_message

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
