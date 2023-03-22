#region DEPENDENCIES
import sys
import dotenv
import requests
import namesgenerator
from flask import Flask

# CONFIGURATION
import config_store
from classes.node import Node
from utils import redis_handler
from utils import logger_handler
from utils import cryptography_handler as app_security
from utils import node_handler
from utils import json_handler

# ROUTES
from routes import discovery
from routes import communication

# CONSTANTS
from constants import app_constants
#endregion

#region LOCAL CONSTANTS
app = Flask(__name__)
ENV_VARIABLES = None
LOCAL_DEBUG = True
#endregion

#region UTILITIES
def load_configurations():
    if dotenv.load_dotenv(sys.argv[1]):
        global ENV_VARIABLES
        ENV_VARIABLES = dotenv.dotenv_values(sys.argv[1])
    else:
        logger_handler.logging.info('Environment file missing')
        exit()

    config_store.read_config()
    redis_handler.configure_redis(ENV_VARIABLES['node'])

    if LOCAL_DEBUG:
        app_constants.CURRENT_WORKING_DIRECTORY /= f'node/{ENV_VARIABLES["node"]}'
        app_constants.CURRENT_WORKING_DIRECTORY.mkdir(exist_ok=True, parents=True)

    app_security.load_or_create_new_key()
    config_store.NODE_IP = f'{ENV_VARIABLES["host"]}:{ENV_VARIABLES["port"]}'

def register_api_routes():
    app.register_blueprint(discovery.discover_endpoint)
    app.register_blueprint(communication.communicate_endpoint)

def register_child_with_primary():
    name = namesgenerator.get_random_name()
    public_key = app_security.get_public_key()

    node = Node.new(config_store.NODE_IP, public_key, name)
    new_node_request = requests.post(
        f'http://{config_store.APP_CONFIG["primary_node"]}/discover',
        json=node.__dict__
    )

    if new_node_request.ok:
        logger_handler.logging.info(f'New Node {name} registered with primary')
    else:
        logger_handler.logging.info(f'Cannot register node: {new_node_request.status_code} - {new_node_request.content}')
        exit()
    
    new_node_request.close()

def get_cluster_nodes():
    data_nodes = requests.get(
        f'http://{config_store.APP_CONFIG["primary_node"]}/discover',
    )

    if data_nodes.ok:
        logger_handler.logging.info(f'Nodes retrieved: {data_nodes}')
    else:
        logger_handler.logging.info(f'Cannot retrieve node list: {data_nodes.status_code} - {data_nodes.content}')
        exit()
    
    nodes = data_nodes.json()
    data_nodes.close()
    nodes = [json_handler.decode(node, Node) for node in nodes]
    node_handler.store_nodes(nodes)

#endregion

if __name__ == '__main__':
    load_configurations()
    logger_handler.configure_logger()
    register_api_routes()

    if ENV_VARIABLES['node'] != 'PRIMARY':
        register_child_with_primary()
        get_cluster_nodes()

    app.run(host=ENV_VARIABLES['host'], port=ENV_VARIABLES['port'], debug=LOCAL_DEBUG)