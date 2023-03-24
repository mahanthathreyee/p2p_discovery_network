from utils import redis_handler

from constants import redis_constants

def get_primary_node():
    return redis_handler.REDIS.get(redis_constants.PRIMARY_NODE)