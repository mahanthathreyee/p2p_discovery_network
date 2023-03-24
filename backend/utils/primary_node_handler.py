import config_store

from constants.app_constants import NODE_HEALTH

from utils import logger_handler
from utils import redis_handler
from utils import node_handler
from utils import node_health_handler

from constants import redis_constants

def update_primary_node(ip):
    return redis_handler.REDIS.set(redis_constants.PRIMARY_NODE, ip)

def get_primary_node():
    return redis_handler.REDIS.get(redis_constants.PRIMARY_NODE)

def initiate_election():
    logger_handler.logging.info('Initiating leader election')
    nodes = node_handler.get_nodes()
    
    higher_leader_val_exists = False
    for node in nodes:
        if node.health == NODE_HEALTH.ONLINE.name and node.node_leader_value > config_store.NODE_LEADER_VALUE:
            higher_leader_val_exists = True
            break
    
    if not higher_leader_val_exists:
        logger_handler.logging.info('Current node with highest value, electing self as primary')
        
        logger_handler.logging.info('Stopping child NODE_RETRIEVAL_PROCESS')
        node_handler.stop_node_retrieval()
        
        update_primary_node(config_store.NODE_IP)
        node_health_handler.init_health_check_thread()
        logger_handler.logging.info('Current node elected as leader')