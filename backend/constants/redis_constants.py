REDIS_KEYS = {
    'NODE_DICT': 'nodes',
    'MESSAGES': 'messages',
    'FILE_SEARCH': 'file_search',
    'DATA_FILES': 'data_files'
}

def configure(prefix: str):
    for k, v in REDIS_KEYS.items():
        REDIS_KEYS[k] = prefix + ":" + v