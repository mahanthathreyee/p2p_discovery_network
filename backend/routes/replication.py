from utils import logger_handler
from utils import request_handler
from replication import replication_handler

from flask import Blueprint, request

replication_endpoint = Blueprint(
    'replication_endpoint', 
    __name__, 
    template_folder='templates',
    url_prefix='/replication'
)

@replication_endpoint.get('/initiate')
def initiate_replication():
    replication_handler.initiate_replication()
    return {'status': 'SUCCESS'}, 200

@replication_endpoint.post('/select_nodes')
def select_replicate_nodes():
    body = request.json
    if not request_handler.check_request_json(body, ['requestor']):
        return 'Bad Request', 400
    
    return replication_handler.select_nodes(body['requestor']), 200

@replication_endpoint.post('/request_replication')
def replicate_data():
    body = request.json
    if not request_handler.check_request_json(body, ['files','requestor']):
        return 'Bad Request', 400
    replication_handler.replicate_data(body['files'], body['requestor'])
    return {'status': 'SUCCESS'}, 200

