from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import functools
import models

rooms_bp = Blueprint("rooms", __name__, url_prefix="/rooms")

def roles_required(*roles):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper

@rooms_bp.route("/")
@login_required
@roles_required("admin","manager")
def list_rooms():
    rs = models.get_all_rooms()
    return render_template("rooms.html", rooms=rs)

@rooms_bp.route("/add", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def add_room():
    if request.method == "POST":
        models.create_room(
          request.form["roomName"],
          request.form["capacity"]
        )
        flash("Room added.", "success")
        return redirect(url_for("rooms.list_rooms"))
    return render_template("add_room.html")

@rooms_bp.route("/edit/<int:rid>", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def edit_room(rid):
    if request.method == "POST":
        models.update_room(
          rid,
          request.form["roomName"],
          request.form["capacity"]
        )
        flash("Room updated.", "success")
        return redirect(url_for("rooms.list_rooms"))
    r = models.get_room_by_id(rid)
    return render_template("edit_room.html", room=r)

@rooms_bp.route("/delete/<int:rid>", methods=["POST"])
@login_required
@roles_required("admin","manager")
def delete_room(rid):
    models.delete_room(rid)
    flash("Room deleted.", "warning")
    return redirect(url_for("rooms.list_rooms"))