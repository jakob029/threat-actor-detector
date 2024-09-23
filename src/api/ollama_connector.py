'''
Handle ollama connection requests.

Classes:
    OllamaConfig

Functions:
    parse_config(config_path) -> OllamaConfig
    test()
'''

import tomllib
import logging
from datetime import date

from ollama import Client

logging.basicConfig(filename=f'ollama-connector-{date.today()}.log', level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaConfig:
    '''
    Class to represent a Ollama config.

    Attributes:
        address: str
            Host address (IP).
        port: str
            Open port ollama listens on.

    Methods:
        get_url(): str
            Returns 'http://<address>:<port>'
    '''


    def __init__(self, config: dict) -> None:
        self.address = config["Host"]["Address"]
        self.port = config["Host"]["Port"]


    def get_url(self) -> str:
        '''
        Returns full ollama  url.

            Returns:
                url : str
                    full url
        '''
        
        return f"http://{self.address}:{self.port}"


def parse_config(config_path: str) -> OllamaConfig:
    '''
    Reads config.toml and returns the parsed content as a OllamaConfig 
    object.

        Returns:
            ollama_config : OllamaConfig
                Ollama config object
    '''

    ollama_config: OllamaConfig

    logger.info(f'Opening {config_path}.')
    with open(config_path, "rb") as f:
        logger.debug(f'Reading {config_path}.')
        data = tomllib.load(f)
        ollama_config = OllamaConfig(data)
    
    logger.info(f'Closed {config_path}.')

    return ollama_config


def test():
    '''
    Loads current config and sens test request to ollama.
    '''

    logging.info('Testing connection with a request.')
    config: OllamaConfig = parse_config('config.toml')
    client: Client = Client(config.get_url())
    response = client.chat(model="llama3.1", messages=[{"role": "user", "content": "what is a rock?"}])

    print(response)
    

