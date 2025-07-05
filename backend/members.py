from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import functools
import models

members_bp = Blueprint("members", __name__, url_prefix="/members")

def roles_required(*roles):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper

@members_bp.route("/")
@login_required
@roles_required("admin","manager","trainer")
def list_members():
    ms = models.get_all_members()
    return render_template("members.html", members=ms)

@members_bp.route("/add", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def add_member():
    if request.method == "POST":
        models.create_member(
          request.form["firstName"],
          request.form["lastName"],
          request.form["email"]
        )
        flash("Member added.", "success")
        return redirect(url_for("members.list_members"))
    return render_template("add_member.html")

@members_bp.route("/edit/<int:mid>", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def edit_member(mid):
    if request.method == "POST":
        models.update_member(
          mid,
          request.form["firstName"],
          request.form["lastName"],
          request.form["email"]
        )
        flash("Member updated.", "success")
        return redirect(url_for("members.list_members"))
    m = models.get_member_by_id(mid)
    return render_template("edit_member.html", member=m)

@members_bp.route("/delete/<int:mid>", methods=["POST"])
@login_required
@roles_required("admin","manager")
def delete_member(mid):
    models.delete_member(mid)
    flash("Member deleted.", "warning")
    return redirect(url_for("members.list_members"))