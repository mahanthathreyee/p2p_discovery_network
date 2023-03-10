#region DEPENDENCIES
from flask import Flask
import dotenv

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
        ENV_VARIABLES = dotenv.dotenv_values(app_constants.MAIN_ENVIRONMENT_FILE)

def register_api_routes():
    app.register_blueprint(discovery.simple_page)

if __name__ == '__main__':
    load_configurations()
    register_api_routes()
    app.run(host=ENV_VARIABLES['host'], port=ENV_VARIABLES['port'], debug=True)