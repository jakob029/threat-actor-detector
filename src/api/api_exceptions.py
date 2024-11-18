"""The different exceptions the api might raise.

Classes:
    ConfigException

"""

USER_DOES_NOT_EXIST = 0
USER_ALREADY_EXIST = 1
USERNAME_TOO_LONG = 2
PASSWORD_DOES_NOT_MATCH = 3
PASSWORD_TOO_WEAK = 4


class AuthenticationException(Exception):
    """Raised when a authentication error occurs.

    Attributes:
        message (str): error message.

    """

    def __init__(self, message: str, code: int) -> None:
        """Init the object.

        Arguments:
            message (str): the error message.
            code (int): error code.

        """
        self.message = message
        self.code = code


class RegistrationException(Exception):
    """Raised when a registration error occurs.

    Attributes:
        message (str): error message.

    """

    def __init__(self, message: str, code: int) -> None:
        """Init Object.

        Arguments:
            message (str): error message.
            code (int): error code.

        """
        self.message = message
        self.code = code
