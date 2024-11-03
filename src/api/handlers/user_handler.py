"""Module to handle all user related functions.

Functions:
    register(username, password)
    authenticate(username, password) -> str

"""

import logging
from argon2 import PasswordHasher
from backend_connectors import get_password_hash, get_user_id
from api_exceptions import AuthenticationException

logger = logging.getLogger(__name__)


def register(username: str, password: str):
    """Register a new user.

    Arguments:
        username (str): Username
        password (str): Users password

    """
    ph: PasswordHasher = PasswordHasher()

    hash = ph.hash(password)

    logger.debug(f"Created user, Username: {username} | Password: {hash}")


def authenicate(username: str, password: str) -> str:
    """Authenticate the user.

    Arguments:
        username (str): Username
        password (str): Users password

    Returns:
        (int): userid

    """
    ph: PasswordHasher = PasswordHasher()

    hash = get_password_hash(username)
    ph.verify(hash, password)

    logger.debug(f"Authentication succeeded for user / password {username} / {password}")
    return get_user_id(username)
