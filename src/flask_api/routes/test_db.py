from flask import Blueprint, jsonify, request
from flask_api.app import db
from flask_api.models import Credential
from flask_api.models.file_entry import FileEntry
import os
import zipfile
import tempfile
from flask import send_file
import rarfile
import py7zr

test_db_bp = Blueprint("test_db", __name__, url_prefix="/api")
BASE_PATH = "/home/phuong/Desktop/thuc_tap/Telegram Bot/Downloads"

@test_db_bp.route("/credentials")
def test_db_connection():
    try:
        # Lấy query parameter 'username' từ request
        username = request.args.get('username', None)
        domain = request.args.get('domain', None)
        emailDomain = request.args.get('email_domain', None)
        software = request.args.get('software', None)
        host = request.args.get('host', None)
        localPart = request.args.get('local_part', None)

        # Phân trang
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
        except ValueError:
            return jsonify({"success": False, "error": "page và per_page phải là số nguyên"}), 400

        # Bắt đầu truy vấn
        query = Credential.query

        # Nếu có tham số username, thêm bộ lọc
        if username:
            query = query.filter(Credential.username.ilike(f'%{username}%'))
        if domain:
            query = query.filter(Credential.domain.ilike(f'%{domain}%'))
        if emailDomain:
            query = query.filter(Credential.email_domain.ilike(f'%{emailDomain}%'))
        if software:
            query = query.filter(Credential.software.ilike(f'%{software}%'))
        if host:
            query = query.filter(Credential.host.ilike(f'%{host}%'))
        if localPart:
            query = query.filter(Credential.local_part.ilike(f'%{localPart}%'))
        
        credentials = query.all()
        # Chuyển các bản ghi thành danh sách các dictionary
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        data = [credential.to_dict() for credential in paginated.items]
        return jsonify({
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@test_db_bp.route("/file-entries")
def get_file_entries():
    try:
        # Lấy filter nếu có
        name = request.args.get('name', None)
        path = request.args.get('path', None)
        filetype = request.args.get('filetype', None)
        system_dir = request.args.get('system_dir', None)

        # Phân trang
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
        except ValueError:
            return jsonify({"success": False, "error": "page và per_page phải là số nguyên"}), 400

        query = FileEntry.query

        if name:
            query = query.filter(FileEntry.name.ilike(f'%{name}%'))
        if path:
            query = query.filter(FileEntry.path.ilike(f'%{path}%'))
        if filetype:
            query = query.filter(FileEntry.filetype.ilike(f'%{filetype}%'))
        if system_dir:
            query = query.filter(FileEntry.system_dir.ilike(f'%{system_dir}%'))

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        data = [entry.to_dict() for entry in paginated.items]

        return jsonify({
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@test_db_bp.route("/open-file")
def open_file():
    try:
        rel_path = request.args.get("path")
        if not rel_path:
            return jsonify({"success": False, "error": "Thiếu path"}), 400

        full_path = os.path.join(BASE_PATH, rel_path)

        # Xử lý .zip
        if ".zip/" in rel_path:
            archive_type = "zip"
            archive_ext = ".zip"
        elif ".rar/" in rel_path:
            archive_type = "rar"
            archive_ext = ".rar"
        elif ".7z/" in rel_path:
            archive_type = "7z"
            archive_ext = ".7z"
        else:
            archive_type = None

        if archive_type:
            archive_part, internal_path = rel_path.split(f"{archive_ext}/", 1)
            archive_file = os.path.join(BASE_PATH, f"{archive_part}{archive_ext}")

            if not os.path.exists(archive_file):
                return jsonify({"success": False, "error": f"Không tìm thấy file {archive_type}"}), 404

            tmp_dir = tempfile.mkdtemp()

            if archive_type == "zip":
                with zipfile.ZipFile(archive_file, 'r') as zf:
                    if internal_path not in zf.namelist():
                        return jsonify({"success": False, "error": "Không tìm thấy file trong zip"}), 404
                    extracted_path = zf.extract(internal_path, path=tmp_dir)

            elif archive_type == "rar":
                with rarfile.RarFile(archive_file, 'r') as rf:
                    if internal_path not in rf.namelist():
                        return jsonify({"success": False, "error": "Không tìm thấy file trong rar"}), 404
                    extracted_path = rf.extract(internal_path, path=tmp_dir)

            elif archive_type == "7z":
                with py7zr.SevenZipFile(archive_file, 'r') as zf:
                    if internal_path not in zf.getnames():
                        return jsonify({"success": False, "error": "Không tìm thấy file trong 7z"}), 404
                    zf.extract(path=tmp_dir, targets=[internal_path])
                    extracted_path = os.path.join(tmp_dir, internal_path)

            return send_file(extracted_path, as_attachment=True)

        else:
            if not os.path.exists(full_path):
                return jsonify({"success": False, "error": "Không tìm thấy file"}), 404

            return send_file(full_path, as_attachment=True)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


