"""Module to handle all user related functions.

"""
import logging
from bcrypt import hashpw

logger = logging.getLogger(__name__)

def register(username: str, password: str):
    from bcrypt import gensalt

    salt: bytes = gensalt()
    password_hash: bytes = hashpw(bytes(password.encode()), salt)

    txt: str = f"Username: {username} | Password: {password_hash} | Salt: {salt}"
    logger.debug(txt)



def sign_in():
    pass


register("user", "pass")
