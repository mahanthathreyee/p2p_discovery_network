from utils import cryptography_handler as app_security
from utils import logger_handler
from utils import redis_handler
from utils import request_handler
from utils import json_handler
from constants.redis_constants import REDIS_KEYS

from classes.message import Message

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
        return 'Bad Request', 400
    
    message = json_handler.decode(body, Message)
    
    redis_handler.REDIS.lpush(REDIS_KEYS['MESSAGES'], json_handler.encode(message))
    return json_handler.encode(message), 201

@communicate_endpoint.get('')
def get_all_messages():
    messages = redis_handler.REDIS.lrange(REDIS_KEYS['MESSAGES'], 0, -1)
    messages = [json.loads(message) for message in messages]

    return messages, 200