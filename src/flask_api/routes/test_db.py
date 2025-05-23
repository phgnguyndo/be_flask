from flask import Blueprint, jsonify
from flask_api.app import db
from sqlalchemy import text

test_db_bp = Blueprint("test_db", __name__, url_prefix="/api")

@test_db_bp.route("/credentials")
def test_db_connection():
    try:
        result = db.session.execute(text("SELECT * FROM db_intern.credentials;"))
        rows = [dict(row._mapping) for row in result]  # Chuyển từng dòng kết quả thành dict
        return jsonify({"success": True, "data": rows})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
