"""The different exceptions the api might raise.

Classes:
    ConfigException
"""


class ConfigException(Exception):
    """Raised when a config error occurs.

    Attributes:
        message (str): error message.
        path (str): config path.
    """

    def __init__(self, path: str, message: str = "Something went wrong with the config.") -> None:
        self.path = path
        self.message = message


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
