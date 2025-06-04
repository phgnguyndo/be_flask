from flask import Blueprint, request, jsonify
from flask_api.app import db
from flask_api.jobs.ingest_json import ingest_new_json_files
from flask_api.jobs.ingest_file_entries import ingest_new_file_entry_jsons
from flask_api.jobs.ingest_news import ingest_news_json
import os
from dotenv import load_dotenv
load_dotenv()

api_bp = Blueprint("api", __name__, url_prefix="/api")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")  # fallback nếu chưa có
ALLOWED_EXTENSIONS = {'.zip', '.rar', '.7z'}

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

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Không có file nào được gửi"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "Tên file trống"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Chỉ cho phép file .zip, .rar, .7z"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(save_path)
        return jsonify({"success": True, "message": "Tải file lên thành công", "path": save_path})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api_bp.route("/trigger-ingest-news", methods=["POST"])
def trigger_ingest_news():
    try:
        ingest_news_json()
        return jsonify({"success": True, "message": "ingested file JSON news"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})