REDIS_KEYS = {
    'NODE_DICT': 'nodes',
    'MESSAGES': 'messages',
    'FILE_SEARCH': 'file_search',
    'DATA_FILES': 'data_files',
    'FILE_SEARCH_PROCESSED': 'file_search_processed'
}

PRIMARY_NODE = 'primary_node'

def configure(prefix: str):
    for k, v in REDIS_KEYS.items():
        REDIS_KEYS[k] = prefix + ":" + v