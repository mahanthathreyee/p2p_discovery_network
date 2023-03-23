from utils import request_handler
from utils import json_handler
from file_discovery import search_helper
from file_discovery import node_file_handler

from flask import Blueprint, request

file_endpoint = Blueprint(
    'file_endpoint', 
    __name__, 
    template_folder='templates',
    url_prefix='/files'
)

@file_endpoint.post('/search')
def search_file():
    body = request.json
    if not request_handler.check_request_json(body, ['file_name']):
        return 'Bad Request', 400
    
    file_name = body['file_name']
    file_search_req = search_helper.search_file(file_name)

    return file_search_req.__dict__, 200

@file_endpoint.get('')
def get_files():
    return list(node_file_handler.get_node_files().values()), 200

@file_endpoint.get('/search/<search_id>')
def get_search_results(search_id: str):
    search_results = search_helper.get_search_results(search_id)
    return search_results.__dict__, 200