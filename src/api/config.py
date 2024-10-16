"""
API configuration module
"""

import tomllib

class Config():
    """
    A class representing the API configurations.

    Attributes:
        llm_address (str): the address of the llm to connect with. 
    """

    def __init__(self) -> None:
        "Initializes Config object."
        
        self.llm_address =  ""


def read_config() -> Config | None:
    """
    Reads thefile ./config/api.toml and loads the configurations into a Config object. 

    Returns:
    Config | None: on success a config obejct will be returned otherwise None.
    """

    conf: dict = {}
    with open("config/api.toml", "rb") as f:
        conf = tomllib.load(f)

    config = Config()

    ### LLM ###
    llm_conf = conf["llm"]

    # Address format
    llm_address = "http://"

    if llm_conf["port"] == 443:
        llm_address = "https://"

    llm_address += llm_conf["host"]

    if llm_conf["port"] != 443 and llm_conf["port"] != 80:
        llm_address += ":"
        llm_address += str(llm_conf["port"])

    config.llm_address = llm_address

    return config


def write_config() -> None:
    """
    Writes the given config to ./config/api.toml.

    Parameter:
    config (Config): config obejct to be written.
    """

    pass
    
