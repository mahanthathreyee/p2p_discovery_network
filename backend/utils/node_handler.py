from constants.redis_constants import REDIS_KEYS
import config_store
from utils import file_handler
from utils import json_handler
from utils import redis_handler
from classes.node import Node
import json

def backup_nodes(nodes):
    node_backup_file = file_handler.get_absolute_file_location(config_store.APP_CONFIG['nodes_backup_file'])
    with open(node_backup_file, 'w') as bkp_file:
        nodes_encoded = [json_handler.encode(node) for node in nodes]
        json.dump(nodes_encoded, bkp_file)

def store_nodes(nodes: list[Node]):
    backup_nodes(nodes)
    node_mapping = {node.ip: json_handler.encode(node) for node in nodes}
    redis_handler.REDIS.hset(REDIS_KEYS['NODE_DICT'], mapping=node_mapping)

def store_node(node: Node):
    redis_handler.REDIS.hset(REDIS_KEYS['NODE_DICT'], node.ip, json_handler.encode(node))

def get_nodes() -> list[Node]:
    nodes = redis_handler.REDIS.hgetall(REDIS_KEYS['NODE_DICT'])
    return [json_handler.decode(v, Node) for v in nodes.values()]

def get_node(ip: str) -> Node:
    node = redis_handler.REDIS.hget(REDIS_KEYS['NODE_DICT'], ip)
    if not node:
        return None
    return json_handler.decode(node, Node)