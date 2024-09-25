from flask import Blueprint, redirect, render_template, request, url_for

from reserve_py.services import reservation_service as service

reservation_bp = Blueprint('reservations', __name__)

@reservation_bp("/login", methods=["POST"])
def login():
    user_id = request.form.get("ID")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    
    user = service.getUser()
    
    if not user or not service.check_valid_user(user.password, password):
        return redirect(url_for("auth.login"), error="ユーザー名またはパスワードが違います")
    
    if user.getRole() == "teacher":
        return redirect(url_for("teacher.list"))
    else:
        return redirect(url_for("student.list"))

