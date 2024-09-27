from flask import Blueprint, redirect, render_template, request, url_for

from reserve_py.services import reservation_service as service

login_bp = Blueprint('login', __name__)


@login_bp.route("/login", methods=["GET"])
def login():
    return render_template("login/login_user.html")


@login_bp.route("/login/submit", methods=["POST"])
def login_post():
    user_id = request.form.get("ID")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    
    user = service.getUser(user_id)
    
    if not user or not service.check_valid_user(user.password, password):
        return redirect(url_for("login"), error="ユーザー名またはパスワードが違います")
    
    if user.getRole() == 0:
        return redirect(url_for("teacher.list"))
    else:
        return redirect(url_for("student.list"))
