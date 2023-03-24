from __future__ import annotations
import time

from constants.app_constants import NODE_HEALTH

class Node:
    def __init__(self):
        self.ip = None
        self.public_key = None
        self.name = None
        self.health = NODE_HEALTH.UNKNOWN.name
        self.last_checked = time.time_ns()
        self.latitude = None
        self.longitude = None
        self.node_leader_value = 0

    def new(ip: str, public_key: str, name: str, latitude: float, longitude: float, health = NODE_HEALTH.UNKNOWN.name, last_checked = time.time_ns()):
        node = Node()
        
        node.ip = ip
        node.public_key = public_key
        node.name = name
        node.health = health
        node.last_checked = last_checked
        node.latitude = latitude
        node.longitude = longitude

        return node