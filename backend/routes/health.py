from utils import logger_handler

from flask import Blueprint

health_endpoint = Blueprint(
    'health_endpoint', 
    __name__, 
    template_folder='templates',
    url_prefix='/health'
)

@health_endpoint.get('')
def get_all_nodes():
    logger_handler.logging.info('Received health check request')
    return {'Status': 'UP'}, 200
