"""Database connector."""

from mysql import connector
import logging
from os import environ

from api_exceptions import AuthenticationException, USER_DOES_NOT_EXIST

logger = logging.getLogger(__name__)

def connect_to_db():
    """Connect to mysql db.

    Returns:
        (PooledMySQLConnection | MySQLConnectionAbstract): Connection

    """
    MYSQL_HOST = environ.get("TAD_MYSQL_HOST")
    MYSQL_USER = environ.get("TAD_MYSQL_USER")
    MYSQL_PASSWORD = environ.get("TAD_MYSQL_PASSWORD")
    MYSQL_DATABASE = environ.get("TAD_MYSQL_DATABASE")

    return connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE)


def username_exist(username: str) -> bool:
    """Check if the username is taken.

    Arguments:
        username (str): user name to check.

    Returns:
        (bool): true if exists otherwise false.

    """
    db = connect_to_db()
    cursor = db.cursor()

    sql = "SELECT auth.username FROM auth WHERE auth.username = %s"
    arg = (username,)

    cursor.execute(sql, arg)
    result = cursor.fetchall()

    cursor.close()
    db.close()

    return len(result) != 0



def get_password_hash(username: str) -> str:
    """Get the hashed password for the user.

    Arguments:
        username (str): username

    """
    db = connect_to_db()
    cursor = db.cursor()

    sql = "SELECT auth.password_hash FROM auth WHERE auth.username = %s"
    arg = (username,)

    cursor.execute(sql, arg)
    resp = cursor.fetchall()

    db.close()

    if len(resp) == 0:
        raise AuthenticationException(
            message = "Username doesn't exist.",
            code = USER_DOES_NOT_EXIST
        )

    hash = str(tuple(resp[0])[0])

    return hash


def get_user_salt(username: str) -> str:
    """Get the salt for the user.

    Arguments:
        username (str): username

    """
    db = connect_to_db()
    cursor = db.cursor()

    sql = "SELECT auth.salt FROM auth WHERE auth.username = %s"
    arg = (username,)

    cursor.execute(sql, arg)
    resp = cursor.fetchall()
    salt = str(tuple(resp[0])[0])


    return salt


def get_user_id(username: str) -> str:
    """Get the ID of the given user.

    Arguments:
        username (str): username

    Returns:
        (str): user id.

    """
    db = connect_to_db()
    cursor = db.cursor()

    sql = "SELECT auth.uid FROM auth WHERE auth.username = %s"
    arg = (username,)

    cursor.execute(sql, arg)
    resp = cursor.fetchall()
    db.close()

    uid = str(tuple(resp[0])[0])

    return uid


def register_user(username: str, hash: str, salt: str):
    """Register new user.

    Arguments:
        username (str): New users username.
        hash (str): password hash.
        salt (str): salt used in the hash.

    """
    db = connect_to_db()
    cursor = db.cursor()
    cursor.callproc("register_new_user", (username, hash, salt))
    cursor.close()
    db.close()


def get_conversations(uid: str) -> list:
    """Get user conversations.

    Arguments:
        uid (str): user id.

    Returns:
        conversations (list): list of user conversations.
 
    """
    db = connect_to_db()
    cursor = db.cursor()
    sql = """
        SELECT conversation.cid, conversation.title 
            FROM conversation 
            WHERE conversation.uid = %s
    """
    cursor.execute(sql, (uid,))

    resps = cursor.fetchall()

    conversations = [{resp[0]: resp[1]} for resp in resps]

    cursor.close()
    db.close()

    return conversations


def get_messages(cid: str) -> list:
    """Get conversation messages.

    Arguments:
        cid (str): conversation id.

    Returns:
        messages (list): list of the messages.

    """
    db = connect_to_db()
    cursor = db.cursor()

    sql = """
        SELECT message.index, message.text, message.role 
            FROM message 
            WHERE message.cid = %s
            ORDER BY message.index
    """

    cursor.execute(sql, (cid,))
    responses = cursor.fetchall()
    messages = [{response[0]: {"role": response[1], "text": response[2]}} for response in responses]

    cursor.close()
    db.close()

    return messages