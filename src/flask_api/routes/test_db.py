from flask import Blueprint, jsonify
from flask_api.app import db
from sqlalchemy import text
from flask_api.models import Credential

test_db_bp = Blueprint("test_db", __name__, url_prefix="/api")

@test_db_bp.route("/credentials")
def test_db_connection():
    try:
        credentials = Credential.query.all()
        # Chuyển các bản ghi thành danh sách các dictionary
        data = [credential.to_dict() for credential in credentials]
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
