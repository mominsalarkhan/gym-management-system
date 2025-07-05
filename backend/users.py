from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import functools
import models
from members import roles_required  # reuse decorator

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
        pwd   = request.form["password"]
        role  = request.form["role"]
        models.create_user(uname, pwd, role)
        flash(f"User {uname} created.", "success")
        return redirect(url_for("users.list_users"))
    return render_template("add_user.html", roles=["admin","manager","trainer","member"])

@users_bp.route("/edit/<int:uid>", methods=["GET","POST"])
@login_required
@roles_required("admin")
def edit_user(uid):
    if request.method == "POST":
        models.update_user(uid,
                           request.form["username"],
                           request.form["role"])
        flash("User updated.", "success")
        return redirect(url_for("users.list_users"))
    u = models.get_user_by_id(uid)
    return render_template("edit_user.html", user=u, roles=["admin","manager","trainer","member"])

@users_bp.route("/delete/<int:uid>", methods=["POST"])
@login_required
@roles_required("admin")
def delete_user(uid):
    models.delete_user(uid)
    flash("User deleted.", "warning")
    return redirect(url_for("users.list_users"))