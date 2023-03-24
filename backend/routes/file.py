from utils import request_handler
from utils import json_handler
from file_discovery import search_helper
from file_discovery import node_file_handler

import io
from flask import Blueprint, request, send_file

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
        return {'status': 'Request fields missing'}, 400
    
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

@file_endpoint.post('/download')
def download_file():
    body = request.json
    if not request_handler.check_request_json(body, ['file_name']):
        return {'status': 'Request fields missing'}, 400

    file = node_file_handler.get_file(body['file_name'])
    if file:
        return send_file(file), 200
    return {'status': 'File not found'}, 404

@file_endpoint.post('/secure/download')
def download_file_securely():
    body = request.json
    if not request_handler.check_request_json(body, ['file_name', 'key']):
        return {'status': 'Request fields missing'}, 400
    
    encrypted_file = node_file_handler.get_file_securely(body['file_name'], body['key'])
    if encrypted_file:
        return send_file(
            io.BytesIO(encrypted_file),
            download_name=body['file_name']
        ), 200
    return {'status': 'File not found'}, 404

@file_endpoint.post('/secure/download_to_node')
def download_file_securely_to_node():
    body = request.json
    if not request_handler.check_request_json(body, ['file_name', 'owner']):
        return {'status': 'Request fields missing'}, 400
    
    success = node_file_handler.download_file_securely(body['file_name'], body['owner'])
    if success:
        return {'status': 'File downloaded'}, 200
    else:
        return {'status': 'File not found'}, 404
