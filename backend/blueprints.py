from flask import Blueprint

main = Blueprint('main', __name__)

# Import routes after blueprint creation to avoid circular dependencies
# Don't import routes here, instead import blueprint in routes.py

