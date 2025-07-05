from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
import models

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        pwd   = request.form["password"]
        user  = models.get_user_by_username(uname)
        if user and check_password_hash(user.PasswordHash, pwd):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login")) 