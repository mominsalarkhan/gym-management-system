from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from members import roles_required
import models

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/")
@login_required
@roles_required("admin")
def list_users():
    us = models.get_all_users()
    return render_template("users.html", users=us)

@users_bp.route("/add", methods=["GET","POST"])
@login_required
@roles_required("admin")
def add_user():
    if request.method == "POST":
        uname = request.form["username"]
        pwd   = request.form["password"]   # raw password
        role  = request.form["role"]
        models.create_user(uname, pwd, role)  # hashing happens in model
        flash(f"User {uname} created.", "success")
        return redirect(url_for("users.list_users"))
    return render_template("add_user.html", roles=["admin","manager","trainer","member"])

@users_bp.route("/edit/<int:uid>", methods=["GET","POST"])
@login_required
@roles_required("admin")
def edit_user(uid):
    user = models.get_user_by_id(uid)
    if request.method == "POST":
        username = request.form["username"]
        role     = request.form["role"]
        pwd      = request.form.get("password")  # optional raw new password

        if pwd:
            models.update_user_password(uid, pwd)  # hashing in model

        models.update_user(uid, username, role)
        flash("User updated.", "success")
        return redirect(url_for("users.list_users"))
    return render_template("edit_user.html", user=user, roles=["admin","manager","trainer","member"])

@users_bp.route("/delete/<int:uid>", methods=["POST"])
@login_required
@roles_required("admin")
def delete_user(uid):
    models.delete_user(uid)
    flash("User deleted.", "warning")
    return redirect(url_for("users.list_users"))