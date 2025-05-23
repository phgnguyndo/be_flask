from flask import Blueprint, jsonify
from flask_api.app import db
from flask_api.jobs.ingest_json import ingest_new_json_files

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/trigger-ingest", methods=["POST"])
def trigger_ingest():
    try:
        ingest_new_json_files()
        return jsonify({"success": True, "message": "Đã quét và đẩy JSON vào DB"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
