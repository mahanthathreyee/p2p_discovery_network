#region DEPENDENCIES
import constants.app_constants as app_constants
import utils.file_handler as file_handler

import json
#endregion

#region CONFIGURATIONS
APP_CONFIG = {}
#endregion

#region UTILITIES
def read_config():
    global APP_CONFIG
    APP_CONFIG = file_handler.read_json(app_constants.CONFIG_FILE)

    print(json.dumps(APP_CONFIG, indent=4))
    print("Application has been configured")
#endregion