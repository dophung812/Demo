from flask import Blueprint

api_bp = Blueprint('api', __name__)

def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
