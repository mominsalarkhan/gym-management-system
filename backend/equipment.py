from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import functools
import models
from members import roles_required

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")

@equipment_bp.route("/")
@login_required
@roles_required("admin","manager")
def list_equipment():
    items = models.get_all_equipment()
    return render_template("equipment.html", equipment=items)

@equipment_bp.route("/add", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def add_equipment():
    if request.method == "POST":
        models.create_equipment(
          request.form["equipmentName"],
          request.form["purchaseDate"],
          request.form["condition"],
          request.form["roomID"]
        )
        flash("Equipment added.", "success")
        return redirect(url_for("equipment.list_equipment"))
    rooms = models.get_all_rooms()
    return render_template("add_equipment.html", rooms=rooms)

@equipment_bp.route("/edit/<int:eid>", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def edit_equipment(eid):
    if request.method == "POST":
        equipment_name = request.form.get("equipmentName")
        purchase_date = request.form.get("purchaseDate")
        condition = request.form.get("condition")
        room_id = request.form.get("roomID")

        models.update_equipment(
            eid,
            equipment_name,
            purchase_date,
            condition,
            room_id
        )
        flash("Equipment updated.", "success")
        return redirect(url_for("equipment.list_equipment"))

    item = models.get_equipment_by_id(eid)
    rooms = models.get_all_rooms()
    return render_template("edit_equipment.html", equipment=item, rooms=rooms)

@equipment_bp.route("/delete/<int:eid>", methods=["POST"])
@login_required
@roles_required("admin","manager")
def delete_equipment(eid):
    models.delete_equipment(eid)
    flash("Equipment removed.", "warning")
    return redirect(url_for("equipment.list_equipment"))