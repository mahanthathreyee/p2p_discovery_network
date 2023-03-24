import config_store

from constants.redis_constants import REDIS_KEYS

from utils import file_handler
from utils import json_handler
from utils import redis_handler
from utils import logger_handler
from utils import primary_node_handler
from utils.repeated_timer_util import RepeatedTimer

from classes.node import Node

import json
import requests
import random

NODE_RETRIEVAL_INTERVAL = 15
NODE_RETRIEVAL_THREAD = None

def backup_nodes(nodes):
    node_backup_file = file_handler.get_absolute_file_location(config_store.APP_CONFIG['nodes_backup_file'])
    with open(node_backup_file, 'w') as bkp_file:
        nodes_encoded = [json_handler.encode(node) for node in nodes]
        json.dump(nodes_encoded, bkp_file)

def store_nodes(nodes: list[Node]):
    backup_nodes(nodes)
    node_mapping = {node.ip: json_handler.encode(node) for node in nodes}
    redis_handler.REDIS.hset(REDIS_KEYS['NODE_DICT'], mapping=node_mapping)

def store_node(node: Node) -> Node:
    if node.node_leader_value == -1:
        node_vals = [n.node_leader_value for n in get_nodes()]
        while new_val := random.randint(0, 65535): 
            if new_val not in node_vals: break
        node.node_leader_value = new_val

    redis_handler.REDIS.hset(REDIS_KEYS['NODE_DICT'], node.ip, json_handler.encode(node))
    return node

def get_nodes() -> list[Node]:
    nodes = redis_handler.REDIS.hgetall(REDIS_KEYS['NODE_DICT'])
    return [json_handler.decode(v, Node) for v in nodes.values()]

def get_node(ip: str) -> Node:
    node = redis_handler.REDIS.hget(REDIS_KEYS['NODE_DICT'], ip)
    if not node:
        return None
    return json_handler.decode(node, Node)

def get_cluster_nodes():
    try: 
        data_nodes = requests.get(
            f'http://{primary_node_handler.get_primary_node()}/discover',
        )
    except Exception as e:
        # Leader is down
        logger_handler.logging.info(f'An error occurred while attempting to retrieve node list: {e}')
        logger_handler.logging.info('Primary unavailable')
        primary_node_handler.initiate_election()
        return

    nodes = None
    if data_nodes.ok:
        nodes = data_nodes.json()
        logger_handler.logging.info(f'Nodes retrieved: {nodes}')
    else:
        logger_handler.logging.info(f'Cannot retrieve node list: {data_nodes.status_code} - {data_nodes.content}')
    
    data_nodes.close()
    nodes = [json_handler.decoder(node, Node) for node in nodes]
    store_nodes(nodes)

def init_node_retrieval():
    global NODE_RETRIEVAL_THREAD
    NODE_RETRIEVAL_THREAD = RepeatedTimer(
        NODE_RETRIEVAL_INTERVAL,
        get_cluster_nodes
    )

def stop_node_retrieval():
    global NODE_RETRIEVAL_THREAD
    if NODE_RETRIEVAL_THREAD:
        NODE_RETRIEVAL_THREAD.stop()