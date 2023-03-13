REDIS_KEYS = {
    'REDIS_NODE_DICT': 'nodes'
}

def configure(prefix: str):
    for k, v in REDIS_KEYS.items():
        REDIS_KEYS[k] = prefix + ":" + v