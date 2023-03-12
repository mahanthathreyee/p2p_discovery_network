#region DEPENDENCIES
from constants.logger_constants import *
import config_store
import logging
import sys
#endregion

#region CONSTANTS
LOGGER_CONFIGURATION = 'INFO'
LOGGER_NAME = 'p2p_logger'
#endregion

#region UTILITIES
def __get_console_handler() ->logging.Handler:
    return logging.StreamHandler(stream=sys.stdout)
#endregion

def configure_logger() -> logging.Logger:
    logger_level = logging.getLevelName(LOGGER_CONFIGURATION)
    handlers = [__get_console_handler()]
    logging.basicConfig(
        level=logger_level, 
        handlers=handlers, 
        format=DEFAULT_LOGGER_FORMAT
    )

def get_logger(logger_name: str = LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(logger_name)