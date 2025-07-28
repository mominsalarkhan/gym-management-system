from flask import Blueprint, render_template, request, redirect, url_for
import models
from flask_login import login_required, current_user
from functools import wraps

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")

# ── Admin-only decorator ──
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            return "Access denied", 403
        return f(*args, **kwargs)
    return decorated_function

# ── Routes ──

@staff_bp.route("/")
@login_required
def list_staff():
    staff = models.get_all_staff()
    return render_template("staff.html", staff=staff)

@staff_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_staff():
    if request.method == "POST":
        first = request.form["first"]
        last = request.form["last"]
        email = request.form["email"]
        role = request.form.get("role", "staff")
        models.create_staff(first, last, email, role)
        return redirect(url_for("staff.list_staff"))
    return render_template("add_staff.html")

@staff_bp.route("/<int:sid>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_staff(sid):
    staff = models.get_staff_by_id(sid)
    if not staff:
        return "Staff not found", 404
    if request.method == "POST":
        first = request.form["first"]
        last = request.form["last"]
        email = request.form["email"]
        role = request.form.get("role", "staff")
        models.update_staff(sid, first, last, email, role)
        return redirect(url_for("staff.list_staff"))
    return render_template("edit_staff.html", staff=staff)

@staff_bp.route("/<int:sid>/delete", methods=["POST"])
@login_required
@admin_required
def delete_staff(sid):
    models.delete_staff(sid)
    return redirect(url_for("staff.list_staff"))