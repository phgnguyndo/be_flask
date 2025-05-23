from flask import Blueprint, jsonify
from flask_api.app import db
from sqlalchemy import text  # <-- Thêm dòng này

test_db_bp = Blueprint("test_db", __name__, url_prefix="/api")

@test_db_bp.route("/test-db")
def test_db_connection():
    try:
        db.session.execute(text("SELECT 1"))  # <-- Bọc câu lệnh trong text()
        return jsonify({"success": True, "message": "Database connected successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
