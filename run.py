from flask import Flask
from routes import discovery

app = Flask(__name__)
app.register_blueprint(discovery.simple_page)