"""Handle ollama connection requests.

Classes:
    OllamaConfig

Functions:
    parse_config(config_path) -> OllamaConfig
    test()

"""

import tomllib
import logging
from datetime import date

from ollama import Client

logging.basicConfig(filename=f"ollama-connector-{date.today()}.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaConfig:
    """Class to represent a Ollama config.

    Attributes:
        address: str
            Host address (IP).
        port: str
            Open port ollama listens on.

    Methods:
        get_url(): str
            Returns 'http://<address>:<port>'

    """

    def __init__(self, config: dict) -> None:
        """Set the config attributes."""
        self.address = config["Host"]["Address"]
        self.port = config["Host"]["Port"]
        self.model = config["LLM"]["Model"]

    def get_url(self) -> str:
        """Return full ollama  url.

        Returns:
            url : str
                full url

        """
        return f"http://{self.address}:{self.port}"


def parse_config(config_path: str) -> OllamaConfig:
    """Load ollama config and return it.

    Returns:
        ollama_config : OllamaConfig
            Ollama config object

    """
    ollama_config: OllamaConfig

    logger.info(f"Opening {config_path}.")
    with open(config_path, "rb") as f:
        logger.debug(f"Reading {config_path}.")
        data = tomllib.load(f)
        ollama_config = OllamaConfig(data)

    logger.info(f"Closed {config_path}.")

    return ollama_config


def test():
    """Test connectivity to the llm."""
    logging.info("Testing connection with a request.")
    config: OllamaConfig = parse_config("config.toml")
    client: Client = Client(config.get_url())
    response = client.chat(model=config.model, messages=[{"role": "user", "content": "what is a rock?"}])

    print(response)


if __name__ == "__main__":
    test()
