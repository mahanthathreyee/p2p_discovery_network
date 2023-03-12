import json
from pathlib import Path
from constants import app_constants as constants

def get_absolute_file_location(relative_file_location: str) -> Path:
    return constants.CURRENT_WORKING_DIRECTORY / relative_file_location

def read_json(relative_file_location: str) -> object:
    parsed_json = None
    with open(get_absolute_file_location(relative_file_location), 'rb') as json_file:
        parsed_json = json.load(json_file)
    
    return parsed_json