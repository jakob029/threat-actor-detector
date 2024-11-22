"""Database connector."""

from mysql import connector
from mysql.connector import Error
import logging
from os import environ

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
    if host is None: raise DatabaseException("Variable TAD_MYSQL_HOST is not set.", VARIABLE_NOT_SET)
    if user is None: raise DatabaseException("Variable TAD_MYSQL_USER is not set.", VARIABLE_NOT_SET)
    if password is None: raise DatabaseException("Variable TAD_MYSQL_PASSWORD is not set.", VARIABLE_NOT_SET)
    if database is None: raise DatabaseException("Variable TAD_MYSQL_DATABASE is not set.", VARIABLE_NOT_SET)

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

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.username FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            result = cursor.fetchall()

    return len(result) != 0


def get_password_hash(username: str) -> str:
    """Get the hashed password for the user.

    Arguments:
        username (str): username

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = "SELECT user.password_hash FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            resp = cursor.fetchall()

    if len(resp) == 0:
        raise AuthenticationException(message="Username doesn't exist.", code=USER_DOES_NOT_EXIST)

    hash = str(tuple(resp[0])[0])

    return hash


def get_user_salt(username: str) -> str:
    """Get the salt for the user.

    Arguments:
        username (str): username

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.salt FROM user WHERE user.username = %s"
            arg = (username,)
            cursor.execute(sql, arg)
            resp = cursor.fetchall()
            salt = str(tuple(resp[0])[0])

    return salt


def update_user_auth(uid: str, hash: str, salt: str):
    """Update user password hash.

    Arguments:
        uid (str): user id.
        hash: user password hash.
        salt (str): new user salt.
    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            cursor.callproc("update_user_auth", (uid, hash, salt))


def get_user_id(username: str) -> str:
    """Get the ID of the given user.

    Arguments:
        username (str): username

    Returns:
        (str): user id.

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            sql = "SELECT user.uid FROM user WHERE user.username = %s"
            arg = (username,)

            cursor.execute(sql, arg)
            resp = cursor.fetchall()

            uid = str(tuple(resp[0])[0])

    return uid


def register_user(username: str, hash: str, salt: str):
    """Register new user.

    Arguments:
        username (str): New users username.
        hash (str): password hash.
        salt (str): salt used in the hash.

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            cursor.callproc("register_new_user", (username, hash, salt))


### Conversation ###
def create_conversation(uid: str, title: str) -> str:
    """Create a conversation for the user.

    Arguments:
        uid (str): User id.
        title (str): Conversation title.

    Returns:
        cid (str): Conversation id.

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:
            args = (uid, title, 0)
            result_args = cursor.callproc("create_conversation", args)

            # validate tuple return.
            if not isinstance(result_args, tuple):
                raise TypeError()

            # validate str return.
            if not isinstance(result_args[2], str):
                raise TypeError()

            cid = result_args[2]

    return cid


def add_message(text: str, role: str, cid: str) -> None:
    """Add a message to a conversation.

    Arguments:
        text (str): The message.
        role (str): Role of the sender.
        cid (str): Conversation id.

    Raises:
        DatabaseException

    """
    db_config = _load_config()
    try:
        with connector.connect(**db_config) as db:
            with db.cursor() as cursor:
                cursor.callproc("add_message", (text, role, cid))
    except Error as e:
        if e.errno == 45000:
            raise DatabaseException("Conversation does not exist.", CONVERSATION_DOES_NOT_EXIST)
        else:
            raise DatabaseException("Something went wrong.", UNKNOWN_ISSUE)


def end_conversation(uid: str, cid: str) -> None:
    """Delete conversation.

    Arguments:
        uid (str): User id.
        cid (str): Conversation id.

    """
    pass


def get_conversations(uid: str) -> dict:
    """Get user conversations.

    Arguments:
        uid (str): user id.

    Returns:
        conversations (dict): user conversations.

    """
    db_config = _load_config()
    with connector.connect(**db_config) as db:
        with db.cursor() as cursor:

            sql = """
                SELECT conversation.cid, conversation.title
                    FROM conversation
                    WHERE conversation.uid = %s
            """
            cursor.execute(sql, (uid,))

            respsonses = cursor.fetchall()
            conversations = {}
            for response in respsonses:
                conversations.update({response[0]: response[1]})

    return conversations


def get_messages(cid: str) -> list:
    """Get conversation messages.

    Arguments:
        cid (str): conversation id.

    Returns:
        messages (list): list of the messages.

    """
    db_config = _load_config()
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
            messages = [{"role": response[1], "content": response[0]} for response in responses]

    return messages
