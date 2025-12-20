import os
from flask import Flask
from finance.routes import finance_bp
from finance.database import init_db

def create_app():
    # for path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")
    # create flask instance
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["SECRET_KEY"] = "dev-secret-key"
    # database init
    init_db()
    # Register all related routes
    app.register_blueprint(finance_bp)
    return app