from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import get_user_by_username, get_user_by_id, get_db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_obj = get_user_by_username(username)

        if user_obj and check_password_hash(user_obj.PasswordHash, password):
            login_user(user_obj)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        user = current_user  # already a User object

        if not check_password_hash(user.PasswordHash, current_password):
            flash("Incorrect current password", "error")
        elif new_password != confirm_password:
            flash("New passwords do not match", "error")
        else:
            hashed = generate_password_hash(new_password, method="pbkdf2:sha256")
            db = get_db()
            cur = db.cursor()
            cur.execute("UPDATE User SET PasswordHash = %s WHERE UserID = %s", (hashed, user.id))
            db.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for("dashboard"))

    return render_template("change_password.html")