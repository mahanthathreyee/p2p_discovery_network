import config_store

from classes.node import Node

from utils import node_handler
from utils import logger_handler
from file_discovery import node_file_handler

import math
import requests
from pathlib import Path

REPLICATION_COUNT = 2

def haversine_distance(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def initiate_replication():
    logger_handler.logging.info('Initiating replication')
    select_nodes_request = requests.post(
        f'http://{config_store.APP_CONFIG["primary_node"]}/replication/select_nodes',
        json={
            'requestor': config_store.NODE_IP
        }
    )

    if not select_nodes_request.ok: return
    
    selected_nodes = select_nodes_request.json()
    select_nodes_request.close()
    node_files = list(node_file_handler.get_node_files().values())
    
    logger_handler.logging.info(f'Replication nodes selected: {selected_nodes}')
    for node in selected_nodes:
        logger_handler.logging.info(f'Requesting node {node} to replicate')
        replication_request = requests.post(
            f'http://{node}/replication/request_replication',
            json={
                'requestor': config_store.NODE_IP,
                'files': node_files
            }
        )
        replication_request.close()
        logger_handler.logging.info(f'Requested node {node} to replicate')

    logger_handler.logging.info('Replication completed')

def select_nodes(requestor_ip: str) -> list[Node]:
    logger_handler.logging.info(f'Received replication request from {requestor_ip}, selecting replication node')
    nodes = node_handler.get_nodes()
    requestor_node = list(filter(lambda node: node.ip == requestor_ip, nodes))[0]

    node_distances = []
    for node in nodes:
        if node.ip == requestor_ip:
            continue

        distance = haversine_distance(
            lat1=requestor_node.latitude,
            lon1=requestor_node.longitude,
            lat2=node.latitude,
            lon2=node.longitude
        )

        node_distances.append([node.ip, abs(distance)])

    node_distances.sort(key=lambda x: x[1])

    if len(node_distances) <= REPLICATION_COUNT:
        return [ip for ip, _distance in node_distances]

    logger_handler.logging.info(f'Node distances computed: {node_distances}')
    selected_nodes = []
    for _ in range(REPLICATION_COUNT):
        selected_nodes.append(node_distances.pop()[0])

    logger_handler.logging.info(f'Selected nodes: {select_nodes}')
    return selected_nodes

def replicate_data(files: list[str], requestor: str):
    logger_handler.logging.info(f'Replication requested received from {requestor}, replicating files')
    for file in files:
        file_path: Path = node_file_handler.DATA_PATH / file
        if file_path.exists():
            logger_handler.logging.info(f'File {file} already exists, skipping replication')
            continue

        logger_handler.logging.info(f'Downloading file {file}')
        file_download_request = requests.post(
            f'http://{requestor}/files/download',
            json={
                'requestor': config_store.NODE_IP,
                'file_name': file
            }
        )

        if not file_download_request.ok: continue

        with open(file_path, 'wb') as replicated_file:
            replicated_file.write(file_download_request.content)

        logger_handler.logging.info(f'File {file} downloaded and stored')
        file_download_request.close()