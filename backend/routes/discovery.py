from utils import cryptography_handler as app_security
from utils import logger_handler
from utils import request_handler
from utils import json_handler
from utils import node_handler

from classes.node import Node

from flask import Blueprint, request
import json

discover_endpoint = Blueprint(
    'discover_endpoint', 
    __name__, 
    template_folder='templates',
    url_prefix='/discover'
)

@discover_endpoint.post('')
def register_node():
    body = request.json
    if not request_handler.check_request_json(body, ['ip', 'public_key', 'name', 'latitude', 'longitude']):
        return 'Bad Request', 400
    
    logger_handler.logging.info(f'Create node: {body}')
    node = json_handler.decoder(body, Node)
    node_handler.store_node(node)

    return json_handler.encode(node), 200

@discover_endpoint.get('')
def get_all_nodes():
    nodes = node_handler.get_nodes()
    nodes = [v.__dict__ for v in nodes]

    return nodes, 200

@discover_endpoint.get('/<ip>')
def get_node(ip: str):
    node = node_handler.get_node(ip)
    if not node:
        return 'Node not found', 404

    return node, 200