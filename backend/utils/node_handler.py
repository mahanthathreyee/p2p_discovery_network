from utils.redis_handler import REDIS
from constants.redis_constants import REDIS_KEYS
from config_store import APP_CONFIG
from utils import file_handler

def store_nodes(nodes):
    node_backup_file = file_handler.get_absolute_file_location(APP_CONFIG['nodes_backup_file'])
    with open(node_backup_file, 'w') as bkp_file:
        bkp_file.write(node_backup_file)

        