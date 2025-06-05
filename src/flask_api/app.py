from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from flask_api.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    # Test route
    @app.route("/")
    def ping():
        return jsonify({
            "message": "WELCOME TO MY APP",
            "routes": {
                "postData": "/api/trigger-ingest",
                "getCredentials": "/api/credentials",
                "postDataFiles": "/api/trigger-ingest-files",
                "getDataFiles": "/api/file-entries",
                "postFile": "/api/upload",
                "newsfeed": "/api/news",
                "login":'/auth/login',
                "uploadJson": '/api/upload-post-json',
                "postDataJson": '/api/trigger-ingest-json',
                "getDataJson":'/api/get-entries-json'
            }
        })

    from flask_api.routes.api import api_bp
    from flask_api.routes.test_db import test_db_bp
    from flask_api.routes.auth import auth_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(test_db_bp)
    app.register_blueprint(auth_bp)

    return app
