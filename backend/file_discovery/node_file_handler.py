import config_store
from constants import app_constants
from constants.redis_constants import REDIS_KEYS
from utils import redis_handler
from utils import hash_handler
from utils import cryptography_handler
from utils import node_handler
from utils import logger_handler

import os
import uuid
import requests
import base64
from pathlib import Path

DATA_PATH = None

def load_node_files():
    # TODO Wait time before running updating data list
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

def get_file(file_name: str) -> object:
    file_hash = hash_handler.generate_hash(file_name)
    file = search_node_files(file_hash)
    if file:
        global DATA_PATH
        return DATA_PATH / file
    else:
        return None

def get_file_securely(file_name: str, encryped_key: str):
    key = cryptography_handler.decrypt_data(base64.b64decode(encryped_key))
    return cryptography_handler.encrypt_file(file_name, key)

def download_file_securely(file_name: str, data_holder: str):
    file_hash = hash_handler.generate_hash(file_name)
    download_id = uuid.uuid4()
    transfer_key = f'{file_hash}:{download_id}'
    logger_handler.logging.info(f'Transfer key: {transfer_key}')

    holder_node = node_handler.get_node(data_holder)
    encrypted_key = cryptography_handler.encrypt_data_with_key(transfer_key, holder_node.public_key)
    encrypted_key = base64.b64encode(encrypted_key).decode('utf-8')

    logger_handler.logging.info(f'Encrypted key: {encrypted_key}')
    file_downlaod = requests.post(
        url=f'http://{holder_node.ip}/files/secure/download',
        json={
            'file_name': file_name,
            'key': encrypted_key
        }
    )
    
    if file_downlaod.ok:
        logger_handler.logging.info(f'File downloaded')
        file = cryptography_handler.decrypt_file(file_downlaod.content, transfer_key)
        with open(DATA_PATH / file_name, 'wb') as f:
            f.write(file)
    else:
        logger_handler.logging.info(f'Failed to retrieve file')

def configure():
    global DATA_PATH
    DATA_PATH = app_constants.CURRENT_WORKING_DIRECTORY / config_store.APP_CONFIG['data_path']