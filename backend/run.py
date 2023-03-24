#region DEPENDENCIES
import sys
import dotenv
import requests
import namesgenerator
from flask import Flask
from flask_cors import CORS

# CONFIGURATION
import config_store
from classes.node import Node
from utils import redis_handler
from utils import logger_handler
from utils import node_handler
from utils import redis_handler
from utils import primary_node_handler
from utils import node_health_handler
from utils import cryptography_handler as app_security
from utils.repeated_timer_util import RepeatedTimer
from file_discovery import node_file_handler

# ROUTES
from routes import discovery
from routes import communication
from routes import file
from routes import health
from routes import replication

# CONSTANTS
from constants import app_constants
#endregion

#region LOCAL CONSTANTS
app = Flask(__name__)
CORS(app)
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
    config_store.NODE_IP = f'{ENV_VARIABLES["public_addr"]}:{ENV_VARIABLES["port"]}'

    node_file_handler.configure()

def register_api_routes():
    app.register_blueprint(discovery.discover_endpoint)
    app.register_blueprint(communication.communicate_endpoint)
    app.register_blueprint(file.file_endpoint)
    app.register_blueprint(health.health_endpoint)
    app.register_blueprint(replication.replication_endpoint)

def register_child_with_primary():
    name = ENV_VARIABLES.get('name', namesgenerator.get_random_name())
    public_key = app_security.get_public_key()
    latitude = float(ENV_VARIABLES['latitude'])
    longitude = float(ENV_VARIABLES['longitude'])

    node = Node.new(config_store.NODE_IP, public_key, name, latitude, longitude)
    new_node_request = requests.post(
        f'http://{primary_node_handler.get_primary_node()}/discover',
        json=node.__dict__
    )

    if new_node_request.ok:
        logger_handler.logging.info(f'New Node {name} registered with primary')
        body = new_node_request.json()
        config_store.NODE_LEADER_VALUE =  body['node_leader_value']
    else:
        logger_handler.logging.info(f'Cannot register node: {new_node_request.status_code} - {new_node_request.content}')
        exit()
    
    new_node_request.close()

#endregion

if __name__ == '__main__':
    load_configurations()
    logger_handler.configure_logger()
    register_api_routes()

    if ENV_VARIABLES['node'] != 'PRIMARY':
        register_child_with_primary()
        node_handler.init_node_retrieval()
    else:
        node_health_handler.init_health_check_thread()

    app.run(
        host=ENV_VARIABLES['host'], 
        port=ENV_VARIABLES['port'], 
        debug=LOCAL_DEBUG,
        use_reloader=False
    )
        
    node_handler.stop_node_retrieval()
    node_health_handler.stop_health_check_thread()