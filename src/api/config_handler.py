"""API configuration module.

Classes:
    Config

Functions:
    read_config() -> Config
    write_config(config) -> None
"""

from typing import Any
import tomllib

from api_exceptions import ConfigException


CONFIG_PATH = "config/api.toml"


class Config:
    """A class representing the API configurations.

    Attributes:
        llm_address (str): the address of the llm to connect with.

    """

    def __init__(self) -> None:
        """Initialize Config object."""
        self.llm_address: str = ""
        self.llm_model: str = ""


def read_config() -> Config:
    """Read the file ./config/api.toml and return Config obejct.

    Returns:
        config (Config): on success a config obejct will be returned otherwise None.

    Raises:
        ConfigException: If config error occur.

    """
    conf: dict[str, Any] | None = {}

    # read config file
    try:
        with open(CONFIG_PATH, "rb") as f:
            conf = tomllib.load(f)

    except Exception:
        raise ConfigException(path=CONFIG_PATH)

    config: Config = Config()

    # validate config
    if not isinstance(conf["llm"], dict):
        raise ConfigException(
            path=CONFIG_PATH,
            message="llm is of wrong type.")

    llm_conf: dict[str, Any] = conf["llm"]

    if not isinstance(llm_conf["host"], str):
        raise ConfigException(
            path=CONFIG_PATH,
            message="llm.host is of wrong type, should be string.")

    if not isinstance(llm_conf["model"], str):
        raise ConfigException(
            path=CONFIG_PATH,
            message="llm.model is of wrong type, should be string.")

    if not isinstance(llm_conf["port"], str) and not isinstance(llm_conf["port"], int):
        raise ConfigException(
            path=CONFIG_PATH,
            message="llm.port is of wrong type, should be string or int.")

    if isinstance(llm_conf["port"], str):
        llm_conf["port"] = int(llm_conf["port"])

    ### LLM ###

    # Address format
    llm_address = "http://"

    if llm_conf["port"] == 443:
        llm_address = "https://"

    llm_address += llm_conf["host"]

    if llm_conf["port"] != 443 and llm_conf["port"] != 80:
        llm_address += ":"
        llm_address += str(llm_conf["port"])

    config.llm_address = llm_address

    config.llm_model = llm_conf["model"]

    return config


def write_config(config: Config) -> None:
    """Write the given config to ./config/api.toml.

    Parameter:
    config (Config): config obejct to be written.
    """
    pass
