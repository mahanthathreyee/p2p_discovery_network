from utils import node_handler
from utils import logger_handler
from utils.repeated_timer_util import RepeatedTimer

from constants.app_constants import NODE_HEALTH

from threading import Thread
from threading import Lock
import requests

HEALTH_CHECK_INTERVAL = 15
health_lock_retrieval_semaphone = Lock()
health_check_locks: dict[str, Lock] = {}

def acquire_node_health_check_lock(node_ip: str):
    health_lock_retrieval_semaphone.acquire()
    
    if node_ip not in health_check_locks:
        health_check_locks[node_ip] = Lock()

    health_check_locks[node_ip].acquire()
    health_lock_retrieval_semaphone.release()

def execute_health_check(node_ip: str):
    acquire_node_health_check_lock(node_ip)
    
    node = node_handler.get_node(node_ip)

    node_endpoint = f'http://{node.ip}/health'
    try:
        health_request = requests.get(url=node_endpoint)
        logger_handler.logging.info(f'Node {node_ip} health check status: {health_request.ok}')
        if health_request.ok:
            node.health = NODE_HEALTH.ONLINE.name
        else: 
            node.health = NODE_HEALTH.OFFLINE.name
    except Exception as e:
        logger_handler.logging.info(f'Node {node_ip} health check status: False')
        node.health = NODE_HEALTH.OFFLINE.name

    node_handler.store_node(node)
    health_check_locks[node_ip].release()


def check_status_of_all_nodes():
    health_threads = []
    for node in node_handler.get_nodes():
        thread = Thread(
            target=execute_health_check, 
            args=(node.ip, )
        )
        thread.start()
        health_threads.append(thread)

    for thread in health_threads:
        thread.join()

def init_health_check_thread() -> RepeatedTimer:
    return RepeatedTimer(
        HEALTH_CHECK_INTERVAL,
        check_status_of_all_nodes
    )