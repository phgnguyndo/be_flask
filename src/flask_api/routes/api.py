from flask import Blueprint, jsonify
from flask_api.app import db
from flask_api.jobs.ingest_json import ingest_new_json_files
from flask_api.jobs.ingest_file_entries import ingest_new_file_entry_jsons

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/trigger-ingest", methods=["POST"])
def trigger_ingest():
    try:
        ingest_new_json_files()
        return jsonify({"success": True, "message": "Đã quét và đẩy JSON vào DB"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@api_bp.route("/trigger-ingest-files", methods=["POST"])
def trigger_ingest_file_entries():
    try:
        ingest_new_file_entry_jsons()
        return jsonify({"success": True, "message": "Đã ingest file_entries"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})