from __future__ import annotations
import json

class Node:
    def __init__(self, ip: str, public_key: str, name: str):
        self.ip = ip
        self.public_key = public_key
        self.name = name
    
    def decode(json: str) -> Node:
        return Node(json['ip'], json['public_key'], json['name'])
    
    def json_encode(self):
        return json.dumps(self.__dict__)
    
    def json_decode(json):
        return Node(json['ip'], json['public_key'], json['name'])