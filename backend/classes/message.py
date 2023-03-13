from __future__ import annotations
import json
import time

from constants.app_constants import MESSAGE_TYPE

class Message:
    def __init__(self):
        self.content = None
        self.received_from = None
        self.type = MESSAGE_TYPE.TEXT.name
        self.is_encrypted = False
        self.received_at = time.time_ns()

    def new(content, received_from, type, is_encrypted):
        message = Message()

        message.content = content
        message.received_from = received_from
        message.is_encrypted = is_encrypted
        message.type = type
        message.received_at = time.time_ns()
        
        return message