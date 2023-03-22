import config_store
from classes.node import Node
from classes.message import Message
from classes.file_request import FileSearch

from utils import json_handler
from utils import node_handler
from utils import logger_handler
from utils import redis_handler

from constants import app_constants
from constants.app_constants import MESSAGE_TYPE
from constants.redis_constants import REDIS_KEYS

import hashlib
import uuid
import time
import requests
import random

def generate_search_id(file_name: str) -> FileSearch:
    file_search_id = uuid.uuid4
    file_hash = hashlib.sha256(file_name)

    file_search_request = FileSearch.new(
        file_hash=file_hash, 
        file_name=file_name, 
        requestor=config_store.NODE_IP, 
        search_id=file_search_id, 
        requested_at=time.time_ns
    )

    redis_handler.REDIS.hset(
        REDIS_KEYS['FILE_SEARCH'], 
        file_search_id, 
        json_handler.encode(file_search_request)
    )

    return file_search_request

def get_neighbor_nodes(node_count: int) -> set[Node]:
    return set(random.sample(node_handler.get_nodes(), node_count))

def search_file(file_name):
    file_search_request = generate_search_id(file_name)

    file_search_req_message = Message.new(
        content=json_handler.encode(file_search_request),
        sender=config_store.NODE_IP,
        type=MESSAGE_TYPE.FILE_SEARCH_REQUEST,
        is_encrypted=False
    )

    neighbors = get_neighbor_nodes(app_constants.NEIGBOR_NODES)
    for node in neighbors:
        logger_handler.logging.info(f'Requesting neighbor {node.name}@{node.ip} for file')
        node_endpoint = f'{node.ip}/communicate'
        file_search_request = requests.post(
            url=node_endpoint,
            json=file_search_request
        )

        if file_search_request.ok():
            logger_handler.logging.info(f'Requested neighbor {node.name}@{node.ip} for file')

def handle_search_response(response: Message) -> bool:
    search_response: FileSearch = json_handler.decoder(response.content, FileSearch)

    file_search_req = redis_handler.REDIS.hget(
        REDIS_KEYS['FILE_SEARCH'], 
        search_response.search_id
    )

    if not file_search_req:
        return False
    
    file_search_req: FileSearch = json_handler.decoder(file_search_req, FileSearch)
    if response.sender not in file_search_req.responses:
        file_search_req.responses.append([
            response.sender, search_response.response
        ])

    return True

def get_search_results(search_id: str) -> tuple[bool, FileSearch]:
    file_search_req = redis_handler.REDIS.hget(
        REDIS_KEYS['FILE_SEARCH'], 
        search_id
    )

    if file_search_req:
        file_search_req: FileSearch = json_handler.decoder(file_search_req, FileSearch)
        for response in file_search_req.responses:
            if response[1]:
                return True, file_search_req
            
    return False, None