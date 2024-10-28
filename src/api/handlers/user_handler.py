"""Module to handle all user related functions.

"""
import logging
from bcrypt import checkpw, hashpw
from backend_connectors import get_password_hash, get_user_id
from src.api.api_exceptions import AuthenticationException



logger = logging.getLogger(__name__)

def register(username: str, password: str):
    from bcrypt import gensalt

    salt: bytes = gensalt()
    password_hash: bytes = hashpw(bytes(password.encode()), salt)

    txt: str = f"Username: {username} | Password: {password_hash} | Salt: {salt}"
    logger.debug(txt)


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
        raise AuthenticationException("Password doesn't match.")

    return get_user_id(username)
