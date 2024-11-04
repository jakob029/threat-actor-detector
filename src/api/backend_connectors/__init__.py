"""Init for module API"""

from .ollama_connector import send_prompt
from .database_connector import get_user_id, get_password_hash, register_user, get_user_salt, username_exist
from os import environ




