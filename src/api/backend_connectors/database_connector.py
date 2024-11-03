"""Database connector."""

from mysql import connector
import logging
from os import environ

logger = logging.getLogger(__name__)

MYSQL_HOST = environ.get("TAD_MYSQL_HOST")
MYSQL_USER = environ.get("TAD_MYSQL_USER")
MYSQL_PASSWORD = environ.get("TAD_MYSQL_PASSWORD")
MYSQL_DATABASE = environ.get("TAD_MYSQL_DATABASE")

def connect_to_db():
    """Connect to mysql db.

    Returns:
        (PooledMySQLConnection | MySQLConnectionAbstract): Connection"""
    return connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)


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
    db.close()
