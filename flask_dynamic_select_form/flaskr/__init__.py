from flask import Flask
from flaskr.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flaskr import routes
