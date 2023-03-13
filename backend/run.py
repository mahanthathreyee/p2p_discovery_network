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

# ROUTES
from routes import discovery

# CONSTANTS
from constants import app_constants
#endregion

#region INIT
app = Flask(__name__)
ENV_VARIABLES = None
LOCAL_DEBUG = True
#endregion

def load_configurations():
    if dotenv.load_dotenv(sys.argv[1]):
        global ENV_VARIABLES
        ENV_VARIABLES = dotenv.dotenv_values(sys.argv[1])
    else:
        logger_handler.logging.info('Environment file missing')
        exit()

    config_store.read_config()

    if LOCAL_DEBUG:
        app_constants.CURRENT_WORKING_DIRECTORY /= f'node/{ENV_VARIABLES["node"]}'
        app_constants.CURRENT_WORKING_DIRECTORY.mkdir(exist_ok=True, parents=True)

    app_security.load_or_create_new_key()
    redis_handler.configure_redis(ENV_VARIABLES['node'])

def register_api_routes():
    app.register_blueprint(discovery.discover_endpoint)

def register_child_with_primary():
    name = namesgenerator.get_random_name()
    ip = f'{ENV_VARIABLES["host"]}:{ENV_VARIABLES["port"]}' 
    public_key = app_security.get_public_key()

    node = Node(ip, public_key, name)
    new_node = requests.post(
        f'http://{config_store.APP_CONFIG["primary_node"]}/discover',
        json=node.__dict__
    )

    if new_node.ok:
        logger_handler.logging.info(f'New Node {name} registered with primary')
    else:
        logger_handler.logging.info(f'Cannot register node: {new_node.status_code} - {new_node.content}')
        exit()
    
    new_node.close()
    

if __name__ == '__main__':
    load_configurations()
    logger_handler.configure_logger()
    register_api_routes()
    if ENV_VARIABLES['node'] != 'PRIMARY':
        register_child_with_primary()

    app.run(host=ENV_VARIABLES['host'], port=ENV_VARIABLES['port'], debug=LOCAL_DEBUG)