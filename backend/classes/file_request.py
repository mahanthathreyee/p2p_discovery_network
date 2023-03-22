from __future__ import annotations
import time

from constants.app_constants import NODE_HEALTH

class FileSearch:
    def __init__(self):
        self.file_hash = None
        self.file_name = None
        self.requestor = None
        self.search_id = None
        self.requested_at = time.time_ns()
        self.response = False
        self.responses = []

    def new(file_hash: str, file_name: str, requestor: str, search_id: str, requested_at: int):
        file_search = FileSearch()
        
        file_search.file_hash = file_hash
        file_search.file_name = file_name
        file_search.requestor = requestor
        file_search.search_id = search_id
        file_search.requested_at = requested_at
        file_search.response = False
        file_search.responses = []

        return file_search