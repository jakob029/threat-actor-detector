"""Init for module backend_connectors

Constants:
    
    LLM_MODEL: model to run.
    LLM_ADDRESS: ollama address.
    LLM_PREPROMPT_PATH: path to preprompt file.

"""
import os

LLM_MODEL = os.environ.get("LLM_MODEL", default="llama3.2")
LLM_ADDRESS = os.environ.get("LLM_ADDRESS", default="http://100.77.88.10")
LLM_PREPROMPT_PATH = os.environ.get("LLM_PREPROMPT_PATH", default="./prepromt")
