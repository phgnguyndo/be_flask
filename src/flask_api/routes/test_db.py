from flask import Blueprint, jsonify, request
from flask_api.app import db
from flask_api.models import Credential

test_db_bp = Blueprint("test_db", __name__, url_prefix="/api")

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
