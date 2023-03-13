from utils import cryptography_handler as app_security
from utils import logger_handler
from utils import redis_handler
from utils import request_handler
from constants.redis_constants import REDIS_KEYS

from classes.node import Node

from flask import Blueprint, request
import json

discover_endpoint = Blueprint('discover_endpoint', __name__, template_folder='templates')

@discover_endpoint.post('/discover')
def register_node():
    body = request.json
    if not request_handler.check_request_json(body, ['ip', 'public_key', 'name']):
        return 'Bad Request', 400
    
    logger_handler.logging.info(f'Create node: {body}')
    node = Node.decode(body)
    redis_handler.REDIS.hset(REDIS_KEYS['REDIS_NODE_DICT'], node.ip, node.json_encode())

    return body, 200

@discover_endpoint.get('/discover')
def get_all_nodes():
    nodes = redis_handler.REDIS.hgetall(REDIS_KEYS['REDIS_NODE_DICT'])
    nodes = [json.loads(v) for v in nodes.values()]

    return nodes, 200

@discover_endpoint.get('/discover/<ip>')
def get_node(ip: str):
    node = redis_handler.REDIS.hget(REDIS_KEYS['REDIS_NODE_DICT'], ip)
    if not node:
        return 'Node not found', 404

    return node, 200