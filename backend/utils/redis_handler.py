import redis
from constants import redis_constants

#region CONSTANTS
REDIS = None
#endregion

def configure_redis(prefix: str):
    redis_constants.configure(prefix)
    
    global REDIS
    REDIS = redis.Redis(decode_responses=True)
    return REDIS.ping()