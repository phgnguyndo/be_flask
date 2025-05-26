from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    # Test route
    @app.route("/")
    def ping():
        return ({"message": 'WELCOME TO MY APP', "routes": {
            "postData": "/api/trigger-ingest",
            "getCredentials": '/api/credentials',
            "postDataFiles":'/api/trigger-ingest-files',
            "getDataFiles":'/api/file-entries'
        }})

    # Đăng ký Blueprint
    from flask_api.routes.api import api_bp
    from flask_api.routes.test_db import test_db_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(test_db_bp)

    return app
