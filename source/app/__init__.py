# __init__.py
from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Import routes (URL handlers)
from app import routes