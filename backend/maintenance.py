from flask import Blueprint, request, redirect, render_template, url_for, flash
from models import (
    get_all_maintenance_logs,
    create_maintenance_log,
    update_maintenance_resolution,
    get_maintenance_log_by_id,
    get_all_equipment,         
    get_all_users               
)
from models import get_all_users
from models import delete_maintenance_log  

maintenance_bp = Blueprint('maintenance', __name__, template_folder='templates')

@maintenance_bp.route("/maintenance", methods=["GET"])
def get_logs():
    logs = get_all_maintenance_logs()
    return render_template("maintenance_logs.html", logs=logs)

@maintenance_bp.route("/maintenance/logs/new", methods=["GET", "POST"])
def add_maintenance_log():
    users = get_all_users()
    equipment = get_all_equipment()

    if request.method == "POST":
        try:
            create_maintenance_log(
                EquipmentID=request.form["EquipmentID"],
                ReportedBy=request.form["ReportedBy"],
                IssueDescription=request.form["IssueDescription"]
            )
            flash("Maintenance log created.", "success")
            return redirect(url_for("maintenance.get_logs"))
        except mysql.connector.IntegrityError:
            flash("Invalid EquipmentID or ReportedBy. Please select valid entries.", "danger")

    return render_template("add_maintenance.html", users=users, equipment=equipment)

@maintenance_bp.route("/maintenance/edit/<int:log_id>", methods=["GET", "POST"])
def edit_maintenance_log(log_id):
    log = get_maintenance_log_by_id(log_id)
    if not log:
        flash("Log not found.", "danger")
        return redirect(url_for("maintenance.get_logs"))

    users = get_all_users()  # You'll need this for the dropdown to repopulate

    if request.method == "POST":
        try:
            update_maintenance_resolution(
                log_id,
                ResolutionStatus=request.form["ResolutionStatus"],
                ResolutionNotes=request.form.get("ResolutionNotes"),
                ResolvedBy=request.form.get("ResolvedBy") or None,
                ResolveDate=request.form.get("ResolveDate") or None
            )
            flash("Maintenance log updated successfully.", "success")
            return redirect(url_for("maintenance.get_logs"))
        except mysql.connector.IntegrityError:
            flash("Invalid ResolvedBy user ID. Please select a valid user.", "danger")

    return render_template("edit_maintenance.html", log=log, users=users)

@maintenance_bp.route("/maintenance/delete/<int:log_id>", methods=["POST"])
def delete_maintenance_log_route(log_id):
    try:
        delete_maintenance_log(log_id)
        flash("Maintenance log deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting log: {str(e)}", "danger")
    return redirect(url_for("maintenance.get_logs"))