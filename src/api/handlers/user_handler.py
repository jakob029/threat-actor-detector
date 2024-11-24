"""Module to handle all user related functions.

Functions:
    register(username, password)
    authenticate(username, password) -> str

"""

import logging
import secrets
from re import findall
from argon2 import PasswordHasher
from backend_connectors.database_connector import (
    username_exist,
    register_user,
    get_user_id,
    update_user_auth,
    get_password_hash,
    get_user_salt,
)
from api_exceptions import (
    PASSWORD_TOO_WEAK,
    USER_ALREADY_EXIST,
    USER_DOES_NOT_EXIST,
    USERNAME_TOO_LONG,
    AuthenticationException,
    RegistrationException,
)

logger = logging.getLogger(__name__)


def register(username: str, password: str):
    """Register a new user.

    Arguments:
        username (str): Username
        password (str): Users password

    Raises:
        RegistrationException: PASSWORD_TOO_WEAK | USERNAME_TOO_LONG | USER_ALREADY_EXIST
        DatabaseException: VARIABLE_NOT_SET | UNKOWN_ISSUE
        TypeError:

    """
    # Validate password strength
    password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if len(findall(password_regex, password)) == 0:
        raise RegistrationException("Password is not strong enough.", PASSWORD_TOO_WEAK)

    # validate length of username.
    if len(username) > 40:
        raise RegistrationException("Username too long.", USERNAME_TOO_LONG)

    # validate if the name is unused.
    if username_exist(username):
        raise RegistrationException("Username already taken.", USER_ALREADY_EXIST)

    # generate salt
    salt = str(secrets.token_hex(4))

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

    Raises:
        AuthenticationException: USERNAME_TOO_LONG | USER_DOES_NOT_EXIST
        DatabaseException: VARIABLE_NOT_SET | UNKOWN_ISSUE | USER_DOES_NOT_EXIST
        TypeError
    """
    # validate username length.
    if len(username) > 40:
        raise AuthenticationException("Username too long.", USERNAME_TOO_LONG)

    # Validate if name exists.
    if not username_exist(username):
        raise AuthenticationException("Username does not exist.", USER_DOES_NOT_EXIST)

    # Validate password hash.
    ph: PasswordHasher = PasswordHasher()
    hash: str = get_password_hash(username)
    salt: str = get_user_salt(username)
    ph.verify(hash, password + salt)

    # Get uid.
    uid: str = get_user_id(username)

    # Generate new hash and salt.
    new_salt = str(secrets.token_hex(4))
    new_hash = ph.hash(password + new_salt)

    # Update database.
    update_user_auth(uid, new_hash, new_salt)

    return get_user_id(username)
