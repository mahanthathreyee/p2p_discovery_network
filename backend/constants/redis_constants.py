REDIS_KEYS = {
    'NODE_DICT': 'nodes',
    'MESSAGES': 'messages'
}

def configure(prefix: str):
    for k, v in REDIS_KEYS.items():
        REDIS_KEYS[k] = prefix + ":" + v