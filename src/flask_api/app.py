from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Test route
    # @app.route("/api/ping")
    # def ping():
    #     return jsonify({"message": "pong"})

    # Đăng ký Blueprint
    from flask_api.routes.api import api_bp
    from flask_api.routes.test_db import test_db_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(test_db_bp)

    return app
