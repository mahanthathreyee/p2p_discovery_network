from __future__ import annotations
import time
import uuid

from constants.app_constants import MESSAGE_TYPE

class Message:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.content = None
        self.sender = None
        self.type = MESSAGE_TYPE.TEXT.name
        self.is_encrypted = False
        self.received_at = time.time_ns()

    def new(content, sender, type, is_encrypted, messageId=None):
        message = Message()

        if id: message.id = messageId
        message.content = content
        message.sender = sender
        message.is_encrypted = is_encrypted
        message.type = type
        message.received_at = time.time_ns()
        
        return message
    
    def dict(self):
        d = self.__dict__
        if not isinstance(self.content, str) and not isinstance(self.content, dict):
            d['content'] = self.content.__dict__

        return d