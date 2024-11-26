"""Database connector."""

from os import environ
import logging
from mysql import connector
from mysql.connector import Error


from api_exceptions import (
    CONVERSATION_DOES_NOT_EXIST,
    UNKNOWN_ISSUE,
    VARIABLE_NOT_SET,
    AuthenticationException,
    USER_DOES_NOT_EXIST,
    DatabaseException,
)

logger = logging.getLogger(__name__)


def _load_config() -> dict:
    """Load config from env variables.

    Raises:
        DatabaseException

    Returns:
        config (dict): The configuration.
    """
    # Get variables.
    host = environ.get("TAD_MYSQL_HOST")
    user = environ.get("TAD_MYSQL_USER")
    password = environ.get("TAD_MYSQL_PASSWORD")
    database = environ.get("TAD_MYSQL_DATABASE")

    # Validate variables.
    if host is None:
        raise DatabaseException("Variable TAD_MYSQL_HOST is not set.", VARIABLE_NOT_SET)
    if user is None:
        raise DatabaseException("Variable TAD_MYSQL_USER is not set.", VARIABLE_NOT_SET)
    if password is None:
        raise DatabaseException("Variable TAD_MYSQL_PASSWORD is not set.", VARIABLE_NOT_SET)
    if database is None:
        raise DatabaseException("Variable TAD_MYSQL_DATABASE is not set.", VARIABLE_NOT_SET)

    db_config = {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
    }

    return db_config


def username_exist(username: str) -> bool:
    """Check if the username is taken.

    Arguments:
        username (str): user name to check.

    Returns:
        (bool): true if exists otherwise false.

    Raises:
        DatabaseException: UNKNOWN_ISSUE | VARIABLE_NOT_SET
        TypeError
    """
    db_config = _load_config()
    exist: bool = False
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.username FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            response = cursor.fetchall()

            if response is None:
                raise DatabaseException("Didn't get a valid response from database.", UNKNOWN_ISSUE)
            if not isinstance(response, list):
                raise TypeError(f"Expected tuple, got type {type(response)}, in {username_exist.__name__}.")

            exist = len(response) != 0

    return exist


def get_password_hash(username: str) -> str:
    """Get the hashed password for the user.

    Arguments:
        username (str): username

    Raises:
        DatabaseException: UNKNOWN_ISSUE | VARIABLE_NOT_SET
        AuthenticationException: USER_DOES_NOT_EXIST
        TypeError
    """
    db_config = _load_config()
    password_hash: str = ""
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = "SELECT user.password_hash FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            response = cursor.fetchone()

            if response is None:
                raise DatabaseException("Didn't get a valid response from database.", UNKNOWN_ISSUE)
            if not isinstance(response, tuple):
                raise TypeError(f"Expected tuple, got type {type(response)}, in {get_password_hash.__name__}.")
            if len(response) == 0:
                raise AuthenticationException(message="Username doesn't exist.", code=USER_DOES_NOT_EXIST)
            if not isinstance(response[0], str):
                raise TypeError(f"Expected string, got type {type(response[0])}, in {get_password_hash.__name__}.")

            password_hash = response[0]

    return password_hash


def get_user_salt(username: str) -> str:
    """Get the salt for the user.

    Arguments:
        username (str): username

    Raises:
        DatabaseException: UNKNOWN_ISSUE | VARIABLE_NOT_SET
        TypeError
    """
    db_config = _load_config()
    salt: str = ""
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.salt FROM user WHERE user.username = %s"
            arg = (username,)
            cursor.execute(sql, arg)
            response = cursor.fetchone()

            if response is None:
                raise DatabaseException("Didn't get a valid response from database.", UNKNOWN_ISSUE)
            if not isinstance(response, tuple):
                raise TypeError(f"Expected tuple, got type {type(response)}, in {get_user_salt.__name__}.")
            if not isinstance(response[0], str):
                raise TypeError(f"Expected string, got type {type(response[0])}, in {get_user_salt.__name__}.")

            salt = response[0]

    return salt


def update_user_auth(uid: str, password_hash: str, salt: str):
    """Update user password hash.

    Arguments:
        uid (str): user id.
        password_hash: user password hash.
        salt (str): new user salt.

    Raises:
        DatabaseException: USER_DOES_NOT_EXIST | UNKNOWN_ISSUE | VARIABLE_NOT_SET

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("update_user_auth", (uid, password_hash, salt))
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("User does not exist.", USER_DOES_NOT_EXIST) from err

        raise DatabaseException(str(err.msg), UNKNOWN_ISSUE) from err


def get_user_id(username: str) -> str:
    """Get the ID of the given user.

    Arguments:
        username (str): username

    Returns:
        (str): user id.

    Raises:
        DatabaseException: VARIABLE_NOT_SET | UNKNOWN_ISSUE
        TypeError

    """
    db_config = _load_config()
    uid: str = ""
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.uid FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            response = cursor.fetchone()

            if response is None:
                raise DatabaseException("Didn't get a valid response from database.", UNKNOWN_ISSUE)
            if not isinstance(response, tuple):
                raise TypeError(f"Expected tuple got {type(response)}, in {get_user_id.__name__}")
            if not isinstance(response[0], str):
                raise TypeError(f"Expected string got {type(response[0])}, in {get_user_id.__name__}")

            uid = response[0]

    return uid


def register_user(username: str, password_hash: str, salt: str):
    """Register new user.

    Arguments:
        username (str): New users username.
        password_hash (str): password hash.
        salt (str): salt used in the hash.

    Raises:
        DatabaseException: VARIABLE_NOT_SET | UNKNOWN_ISSUE

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("register_new_user", (username, password_hash, salt))
    except Error as err:
        raise DatabaseException(str(err.msg), UNKNOWN_ISSUE) from err


### Conversation ###
def create_conversation(uid: str, title: str) -> str:
    """Create a conversation for the user.

    Arguments:
        uid (str): User id.
        title (str): Conversation title.

    Returns:
        cid (str): Conversation id.

    Raises:
        DatabaseException: VARIABLE_NOT_SET | USER_DOES_NOT_EXIST | UNKNOWN_ISSUE

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                args = (uid, title, 0)
                result_args = cursor.callproc("create_conversation", args)

                # validate tuple return.
                if not isinstance(result_args, tuple):
                    raise TypeError(f"Expected tuple got {type(result_args)}, in {create_conversation.__name__}")

                # validate str return.
                if not isinstance(result_args[2], str):
                    raise TypeError(f"Expected string got {type(result_args[2])}, in {create_conversation.__name__}")

                cid = result_args[2]
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("User does not exist.", USER_DOES_NOT_EXIST) from err

        raise DatabaseException(str(err.msg), UNKNOWN_ISSUE) from err

    return cid


def add_message(text: str, role: str, cid: str) -> None:
    """Add a message to a conversation.

    Arguments:
        text (str): The message.
        role (str): Role of the sender.
        cid (str): Conversation id.

    Raises:
        DatabaseException: CONVERSATION_DOES_NOT_EXIST | UNKNOWN_ISSUE | VARIABLE_NOT_SET

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("add_message", (text, role, cid))
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("Conversation does not exist.", CONVERSATION_DOES_NOT_EXIST) from err

        raise DatabaseException("Something went wrong.", UNKNOWN_ISSUE) from err


def end_conversation(cid: str) -> None:
    """Delete conversation.

    Arguments:
        cid (str): Conversation id.

    Raises:
        DatabaseException: CONVERSATION_DOES_NOT_EXIST | UNKNOWN_ISSUE | VARIABLE_NOT_SET

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("delete_conversation", (cid,))
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("Conversation does not exist.", CONVERSATION_DOES_NOT_EXIST) from err

        raise DatabaseException("Something went wrong.", UNKNOWN_ISSUE) from err


def get_conversations(uid: str) -> dict:
    """Get user conversations.

    Arguments:
        uid (str): user id.

    Returns:
        conversations (dict): user conversations.

    Raises:
        DatabaseException: VARIABLE_NOT_SET
        TypeError
    """
    db_config = _load_config()
    conversations: dict[str, str] = {}
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = """
                SELECT conversation.cid, conversation.title
                    FROM conversation
                    WHERE conversation.uid = %s
            """
            cursor.execute(sql, (uid,))

            respsonses = cursor.fetchall()
            for response in respsonses:
                if not isinstance(response, tuple):
                    raise TypeError(f"Expected tuple got {type(response)}, in {get_conversations.__name__}")
                if not isinstance(response[0], str):
                    raise TypeError(f"Expected string got {type(response[0])}, in {get_conversations.__name__}")
                if not isinstance(response[1], str):
                    raise TypeError(f"Expected string got {type(response[1])}, in {get_conversations.__name__}")

                conversations.update({response[0]: response[1]})

    return conversations


def get_messages(cid: str) -> list[dict[str, str]]:
    """Get conversation messages.

    Arguments:
        cid (str): conversation id.

    Returns:
        messages (list): list of the messages.

    Raises:
        DatabaseException: VARIABLE_NOT_SET
        TypeError

    """
    db_config = _load_config()
    messages: list[dict[str, str]] = []
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = """
                SELECT message.text, message.role
                    FROM message
                    WHERE message.cid = %s
                    ORDER BY message.index
            """

            cursor.execute(sql, (cid,))
            responses = cursor.fetchall()
            for response in responses:
                if not isinstance(response, tuple):
                    raise TypeError(f"Expected tuple got {type(response)}, in {get_messages.__name__}")
                if not isinstance(response[0], str):
                    raise TypeError(f"Expected string got {type(response[0])}, in {get_messages.__name__}")
                if not isinstance(response[1], str):
                    raise TypeError(f"Expected string got {type(response[1])}, in {get_messages.__name__}")

                messages += [{"content": response[0], "role": response[1]}]

    return messages


def get_graph(cid: str) -> dict[str, int]:
    """Get data points for graph and return them.

    Arguments:
        cid (str): conversation id.

    Returns:
        data_points (dict[str, int]): the different data points.

    Raises:
        DatabaseException: VARIABLE_NOT_SET
        TypeError
    """
    db_config = _load_config()
    data_points: dict[str, int] = {}
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = """
                SELECT graph.name, graph.value
                    FROM graph
                    WHERE graph.cid = %s
                    ORDER BY graph.name
            """

            cursor.execute(sql, (cid,))
            responses = cursor.fetchall()
            for response in responses:
                if not isinstance(response, tuple):
                    raise TypeError(f"Expected tuple, got type {type(response)}.")
                if not isinstance(response[0], str):
                    raise TypeError(f"Expected string, got type {type(response)}.")
                if not isinstance(response[1], int):
                    raise TypeError(f"Expected int, got type {type(response)}.")

                data_points.update({response[0]: int(response[1])})

    return data_points


def add_graph_point(cid: str, name: str, value: int) -> None:
    """Add a data point to the graph.

    Arguments:
        cid (str): conversation id.
        name (str): name of the point.
        value (int): value.

    Raises:
        DatabaseException: CONVERSATION_DOES_NOT_EXIST | UNKNOWN_ISSUE | VARIABLE_NOT_SET
    """
    db_config = _load_config()

    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("add_data_point", (cid, name, value))
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("Conversation does not exist.", CONVERSATION_DOES_NOT_EXIST) from err

        raise DatabaseException(str(err.msg), UNKNOWN_ISSUE) from err


def reset_conversation(cid: str):
    """Remove all messages and graphs related to the conversation.

    Arguments:
        cid (str): conversation id.

    Raises:
        DatabaseException: CONVERSATION_DOES_NOT_EXIST | UNKNOWN_ISSUE | VARIABLE_NOT_SET

    """
    db_config = _load_config()

    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("reset_conversation", (cid,))
    except Error as err:
        if err.errno == 45000:
            raise DatabaseException("Conversation does not exist.", CONVERSATION_DOES_NOT_EXIST) from err

        raise DatabaseException(str(err.msg), UNKNOWN_ISSUE) from err
