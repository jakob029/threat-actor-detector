"""Module to handle all user related functions.

Functions:
    register(username, password)
    authenticate(username, password) -> str

"""

import logging
from bcrypt import checkpw, hashpw, gensalt
from backend_connectors import get_password_hash, get_user_id
from api_exceptions import AuthenticationException

logger = logging.getLogger(__name__)


def register(username: str, password: str):
    """Register a new user.

    Arguments:
        username (str): Username
        password (str): Users password

    """
    salt: bytes = gensalt()
    password_hash: bytes = hashpw(bytes(password.encode()), salt)

    logger.debug(f"Created user, Username: {username} | Password: {password_hash}")


def authenicate(username: str, password: str) -> str:
    """Authenticate the user.

    Arguments:
        username (str): Username
        password (str): Users password

    Returns:
        (int): userid

    """
    password_bytes: bytes = bytes(password.encode())

    if not checkpw(get_password_hash(username), password_bytes):
        logger.debug(f"Authentication failed for user / password {username} / {password}")
        raise AuthenticationException("Password doesn't match.")

    logger.debug(f"Authentication succeeded for user / password {username} / {password}")
    return get_user_id(username)
