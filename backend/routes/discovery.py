from utils import cryptography_handler as app_security
from utils import logger_handler

from flask import Blueprint

simple_page = Blueprint('simple_page', __name__, template_folder='templates')

@simple_page.get('/discover')
def get_known_node_list():
    pass