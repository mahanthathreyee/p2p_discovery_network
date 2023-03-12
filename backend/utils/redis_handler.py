import redis

#region CONSTANTS
REDIS = None
#endregion

def configure_redis():
    global REDIS
    REDIS = redis.Redis(decode_responses=True)
    return REDIS.ping()