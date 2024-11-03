"""Module to handle all user related functions.

Functions:
    register(username, password)
    authenticate(username, password) -> str

"""

import logging
import secrets
from argon2 import PasswordHasher
from backend_connectors import get_password_hash, get_user_id, register_user, get_user_salt
from api_exceptions import AuthenticationException

logger = logging.getLogger(__name__)


def register(username: str, password: str):
    """Register a new user.

    Arguments:
        username (str): Username
        password (str): Users password

    """
    # generate salt
    salt = str(secrets.token_hex(4))
    print(salt)

    # hash password password + salt
    ph: PasswordHasher = PasswordHasher()
    hash = ph.hash(password + salt)

    register_user(username, hash, salt)

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
    hash: str = get_password_hash(username)
    salt: str = get_user_salt(username)
    ph.verify(hash, password + salt)

    return get_user_id(username)
