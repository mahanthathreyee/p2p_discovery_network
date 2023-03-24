from utils import cryptography_handler as app_security
from utils import logger_handler
from utils import redis_handler
from utils import request_handler
from utils import json_handler
from file_discovery import search_helper
from constants.redis_constants import REDIS_KEYS
from constants.app_constants import MESSAGE_TYPE

from classes.message import Message
from classes.file_request import FileSearch

from flask import Blueprint, request
import json

communicate_endpoint = Blueprint(
    'communicate_endpoint', 
    __name__, 
    template_folder='templates',
    url_prefix='/communicate'
)

@communicate_endpoint.post('')
def recieve_message():
    body = request.json
    if not request_handler.check_request_json(body, ['content', 'sender']):
        return {'status': 'Request fields missing'}, 400
    
    logger_handler.logging.info(f'Message received: {body}')
    message: Message = json_handler.decoder(body, Message)
    
    redis_handler.REDIS.lpush(REDIS_KEYS['MESSAGES'], json_handler.encode(message))
    if message.type == MESSAGE_TYPE.FILE_SEARCH_REQUEST.name:
        search_request: FileSearch = json_handler.decoder(message.content, FileSearch)
        search_helper.handle_search_request(search_request)
    elif message.type == MESSAGE_TYPE.FILE_SEARCH_RESPONSE.name:
        search_request: FileSearch = json_handler.decoder(message.content, FileSearch)
        search_helper.handle_search_response(search_request)

    return json_handler.encode(message), 201

@communicate_endpoint.get('')
def get_all_messages():
    messages = redis_handler.REDIS.lrange(REDIS_KEYS['MESSAGES'], 0, -1)
    messages = [json.loads(message) for message in messages]

    return messages, 200