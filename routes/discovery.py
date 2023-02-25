from flask import Blueprint
import os

simple_page = Blueprint('simple_page', __name__, template_folder='templates')

@simple_page.get('/discover')
def get_known_node_list():
    return "<p>Hello, World!</p>"

@simple_page.get('/view_files')
def get_files():
    directory_tree = {}
    key = "/Users/hemanthkota/Downloads/"
    for i in os.listdir('.'):
       if os.path.iffile(i):
          if key in directory_tree:
             directory_tree[key].append(i)
          else:
             directory_tree[key] = [i]
    return directory_tree
