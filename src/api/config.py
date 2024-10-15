import tomllib

class Config():
    def __init__(self) -> None:
        self.llm_address =  ""

def read_config() -> Config | None:
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
    pass
    
