from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_api.models.user import User
from flask_api.app import db, bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "error": "Username đã tồn tại"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "Đăng ký thành công"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "error": "Sai thông tin đăng nhập"}), 401

    login_user(user)
    return jsonify({"success": True, "message": "Đăng nhập thành công"})


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Đăng xuất thành công"})


@auth_bp.route("/me")
@login_required
def get_current_user():
    return jsonify({"success": True, "user": current_user.to_dict()})
