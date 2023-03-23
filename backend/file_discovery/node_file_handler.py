import config_store
from constants import app_constants
from constants.redis_constants import REDIS_KEYS
from utils import redis_handler
from utils import hash_handler

import os
from pathlib import Path

def load_node_files():
    # TODO Wait time before running updating data list

    DATA_PATH: Path = app_constants.CURRENT_WORKING_DIRECTORY / config_store.APP_CONFIG['data_path']
    DATA_PATH.mkdir(exist_ok=True)
    
    node_files = {}
    for file in os.listdir(DATA_PATH):
        file_hash = hash_handler.generate_hash(file)
        node_files[file_hash] = str(file)
    
    if node_files != {}:
        redis_handler.REDIS.hset(
            REDIS_KEYS['DATA_FILES'], 
            mapping=node_files
        )

def get_node_files(start:int=0, end:int=-1) -> dict[str, str]:
    load_node_files()

    if not redis_handler.REDIS.exists(REDIS_KEYS['DATA_FILES']):
        return []
    return redis_handler.REDIS.hgetall(REDIS_KEYS['DATA_FILES'])

def search_node_files(file_hash: str) -> bool:
    load_node_files()
    if not redis_handler.REDIS.exists(REDIS_KEYS['DATA_FILES']):
        return None
    return redis_handler.REDIS.hget(REDIS_KEYS['DATA_FILES'], file_hash)