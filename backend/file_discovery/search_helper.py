import config_store
from classes.node import Node
from classes.message import Message
from classes.file_request import FileSearch

from file_discovery import node_file_handler

from utils import json_handler
from utils import node_handler
from utils import logger_handler
from utils import redis_handler
from utils import hash_handler

from constants import app_constants
from constants.app_constants import MESSAGE_TYPE
from constants.redis_constants import REDIS_KEYS

import uuid
import time
import requests
import random
from threading import Lock

file_search_response_store = Lock()

def generate_search_id(file_name: str) -> FileSearch:
    file_search_id = str(uuid.uuid4())
    file_hash = hash_handler.generate_hash(file_name)

    file_search_request = FileSearch.new(
        file_hash=file_hash, 
        file_name=file_name, 
        requestor=config_store.NODE_IP, 
        search_id=file_search_id, 
        requested_at=time.time_ns()
    )

    redis_handler.REDIS.hset(
        REDIS_KEYS['FILE_SEARCH'], 
        file_search_id, 
        json_handler.encode(file_search_request)
    )

    return file_search_request

def get_neighbor_nodes(node_count: int, nodes_completed: list[str]) -> set[Node]:
    nodes = node_handler.get_nodes()
    nodes = [node for node in nodes if node.ip not in nodes_completed]
    
    if len(nodes) <= node_count:
        return set(nodes)
    
    neighbors = set()
    while len(neighbors) < node_count:
        neighbors.add(nodes[random.randint(0, len(nodes) - 1)])

    return neighbors

def send_response_to_requestor(request: FileSearch):
    file_search_res_message = Message.new(
        content=request,
        sender=config_store.NODE_IP,
        type=MESSAGE_TYPE.FILE_SEARCH_RESPONSE.name,
        is_encrypted=False
    )

    node_endpoint = f'http://{request.requestor}/communicate'
    file_search_request = requests.post(
        url=node_endpoint,
        json=file_search_res_message.dict()
    )

    if file_search_request.ok:
        logger_handler.logging.info(f'Search response sent to requestor for search ID {request.search_id}')

def file_found_handler(request: FileSearch, file_owner: str):
    request.responses[file_owner] = True
    logger_handler.logging.info(f'File found for search ID: {request.search_id} at node {file_owner}')
    
    if request.requestor == file_owner:
        file_search_response_store.acquire()
        logger_handler.logging.info("file_search_response_store lock acquired")

        search_request = redis_handler.REDIS.hget(
            REDIS_KEYS['FILE_SEARCH'], 
            request.search_id
        )

        search_request: FileSearch = json_handler.decoder(search_request, FileSearch)
        search_request.responses[file_owner] = True

        redis_handler.REDIS.hset(
            REDIS_KEYS['FILE_SEARCH'], 
            search_request.search_id, 
            json_handler.encode(search_request)
        )

        logger_handler.logging.info("file_search_response_store lock released")
        file_search_response_store.release()
    else:
        send_response_to_requestor(request)

def forward_file_search_req_to_neighbors(file_search_request: FileSearch):
    file_search_request.responses[config_store.NODE_IP] = False

    neighbors = get_neighbor_nodes(
        app_constants.NEIGBOR_NODES, 
        list(file_search_request.responses.keys())
    )

    for neighbor in neighbors:
        file_search_request.responses[neighbor.ip] = None

    file_search_req_message = Message.new(
        content=file_search_request,
        sender=config_store.NODE_IP,
        type=MESSAGE_TYPE.FILE_SEARCH_REQUEST.name,
        is_encrypted=False
    )

    for node in neighbors:
        logger_handler.logging.info(f'Requesting neighbor {node.name}@{node.ip} for file')
        node_endpoint = f'http://{node.ip}/communicate'

        forward_request = requests.post(
            url=node_endpoint,
            json=file_search_req_message.dict()
        )

        if forward_request.ok:
            logger_handler.logging.info(f'Requested neighbor {node.name}@{node.ip} for file')

    if file_search_request.requestor == config_store.NODE_IP:
        send_response_to_requestor(file_search_request)

def handle_search_request(request: FileSearch):
    logger_handler.logging.info(f'Search request received: {request.__dict__}')
    
    # TODO check if request already handled 
    
    if node_file_handler.search_node_files(request.file_hash):
        file_found_handler(request, config_store.NODE_IP)

    forward_file_search_req_to_neighbors(request)
    
    return request

def search_file(file_name: str) -> bool:
    return handle_search_request(generate_search_id(file_name))
    
def handle_search_response(node_response: FileSearch):
    logger_handler.logging.info(f'Search response received: {node_response}')
    
    file_search_response_store.acquire()
    logger_handler.logging.info("file_search_response_store lock acquired")

    search_response = redis_handler.REDIS.hget(
        REDIS_KEYS['FILE_SEARCH'], 
        node_response.search_id
    )

    search_response: FileSearch = json_handler.decode(search_response, FileSearch)
    for node_ip, file_exists in node_response.responses.items():
        if file_exists != None:
            search_response.responses[node_ip] = file_exists

    redis_handler.REDIS.hset(
        REDIS_KEYS['FILE_SEARCH'], 
        search_response.search_id, 
        json_handler.encode(search_response)
    )

    logger_handler.logging.info("file_search_response_store lock released")
    file_search_response_store.release()

def get_search_results(search_id: str) -> FileSearch:
    file_search_req = redis_handler.REDIS.hget(
        REDIS_KEYS['FILE_SEARCH'], 
        search_id
    )

    if file_search_req:
        return json_handler.decode(file_search_req, FileSearch)
            
    return None