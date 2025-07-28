from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import (
    get_all_events, get_event_by_id, create_calendar_event, delete_event,
    get_all_users, get_all_classes
)

calendar_bp = Blueprint("calendar", __name__, template_folder="templates")

@calendar_bp.route("/calendar")
def calendar_view():
    events = get_all_events()
    return render_template("calendar.html", events=events)

@calendar_bp.route("/calendar/add", methods=["GET", "POST"])
def add_event():
    users = get_all_users()
    classes = get_all_classes()

    if request.method == "POST":
        try:
            create_calendar_event(
                Title=request.form["Title"],
                Description=request.form.get("Description"),
                StartTime=request.form["StartTime"],
                EndTime=request.form["EndTime"],
                Location=request.form.get("Location"),
                CreatedBy=request.form["CreatedBy"],
                EventType=request.form.get("EventType", "other")
            )
            flash("Event added successfully!", "success")
            return redirect(url_for("calendar.calendar_view"))
        except Exception as e:
            flash("Error: Invalid event data. " + str(e), "danger")

    return render_template("add_event.html", users=users, classes=classes)

@calendar_bp.route("/calendar/delete/<int:event_id>", methods=["POST"])
def delete_event_route(event_id):
    delete_event(event_id)
    flash("Event deleted.", "success")
    return redirect(url_for("calendar.calendar_view"))