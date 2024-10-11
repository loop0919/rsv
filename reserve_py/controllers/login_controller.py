from flask import Blueprint, redirect, render_template, request, url_for, make_response

from reserve_py.services import reservation_service as service, utils
from hashlib import sha256

import secrets


login_bp = Blueprint('login', __name__)
sessions = set()


@login_bp.route("/login", methods=["GET"])
def login():
    return render_template("login/login_user.html")


@login_bp.route("/login/submit", methods=["POST"])
def login_post():
    user_id = request.form.get("ID")
    password = request.form.get("pass")
    
    users = utils.load_json("users")
    user = users.get(user_id)
    
    if not user:
        return redirect(url_for("login.login"))

    if hashify(password, user["solt"]) != user["password_hash"]:
        return redirect(url_for("login.login"))
    
    res = make_response(redirect(url_for("reservations.list_default")))
    token = secrets.token_hex(32)
    
    res.set_cookie("session", token)
    sessions.add(token)
    
    return res

def hashify(password, solt):
    hash_val = password + solt
    
    for _ in range(10):
        hash_val = sha256(hash_val.encode()).hexdigest()
    
    return hash_val
