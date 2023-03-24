import os
from pathlib import Path
from enum import Enum

CONFIG_FILE = 'config/config.json'
CURRENT_WORKING_DIRECTORY = Path(os.getcwd())
APP_ENVIRONMENT_FILE = '.env'
NEIGBOR_NODES = 2

class NODE_HEALTH(Enum):
    UNKNOWN = 'UNKNOWN'
    ONLINE = 'ONLINE',
    OFFLINE = 'OFFLINE'

class MESSAGE_TYPE(Enum):
    TEXT = 'TEXT',
    FILE_SEARCH_REQUEST = 'FILE_SEARCH_REQUEST',
    FILE_SEARCH_RESPONSE = 'FILE_SEARCH_RESPONSE'