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
<<<<<<< HEAD

    """

    def __init__(self, message: str, code: int) -> None:
        """Init the object.

        Arguments:
            message (str): the error message.
            code (int): error code.

        """
=======
        path (str): config path.

    """

    def __init__(
            self, path: str,
            message: str = "Something went wrong with the config."
    ) -> None:
        self.path = path
>>>>>>> c80bb9db3d3088714847d20867e2008e8a727d29
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


