#region DEPENDENCIES
from flask import Flask
import dotenv

# CONFIGURATION
import config_store
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
#endregion

def load_configurations():
    if dotenv.load_dotenv():
        global ENV_VARIABLES
        ENV_VARIABLES = dotenv.dotenv_values(app_constants.APP_ENVIRONMENT_FILE)

    config_store.read_config()
    app_security.load_or_create_new_key()

def register_api_routes():
    app.register_blueprint(discovery.simple_page)

if __name__ == '__main__':
    load_configurations()
    logger_handler.configure_logger()
    register_api_routes()
    app.logger.info('testing info log')
    app.run(host=ENV_VARIABLES['host'], port=ENV_VARIABLES['port'], debug=True)