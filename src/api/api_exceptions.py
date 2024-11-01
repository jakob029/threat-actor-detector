"""The different exceptions the api might raise.

Classes:
    ConfigException

"""


class AuthenticationException(Exception):
    """Raised when a authentication error occurs.

    Attributes:
        message (str): error message.

    """

    def __init__(self, message: str) -> None:
        """Init the object.

        Arguments:
            message (str): the error message.

        """
        self.message = message
