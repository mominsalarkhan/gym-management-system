from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import models

classes_bp = Blueprint("classes", __name__, url_prefix="/classes")

@classes_bp.route("/")
@login_required
def list_classes():
    classes = models.get_all_classes()
    schedules = models.get_all_class_schedules()
    attendance = models.get_all_attendance()
    return render_template("classes.html", classes=classes, schedules=schedules, attendance=attendance)

@classes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_class():
    rooms = models.get_all_rooms()
    trainers = models.get_all_trainers()

    if request.method == "POST":
        cname = request.form["class_name"]
        desc = request.form["description"]
        cap = request.form["capacity"]
        rid = request.form["room_id"]
        tid = request.form["trainer_id"]

        # Validate foreign keys
        if not models.get_room_by_id(rid):
            flash("Room ID does not exist.", "danger")
            return render_template("add_class.html", rooms=rooms, trainers=trainers)

        if not models.get_trainer_by_id(tid):
            flash("Trainer ID does not exist.", "danger")
            return render_template("add_class.html", rooms=rooms, trainers=trainers)

        # Create the class if everything is valid
        models.create_fitness_class(cname, cap, rid, tid, desc)
        return redirect(url_for("classes.list_classes"))

    return render_template("add_class.html", rooms=rooms, trainers=trainers)

@classes_bp.route("/edit/<int:cid>", methods=["GET", "POST"])
@login_required
def edit_class(cid):
    class_data = models.get_class_by_id(cid)
    rooms = models.get_all_rooms()
    trainers = models.get_all_trainers()
    if request.method == "POST":
        cname = request.form["class_name"]
        desc = request.form["description"]
        cap = request.form["capacity"]
        rid = request.form["room_id"]
        tid = request.form["trainer_id"]
        models.update_fitness_class(cid, cname, desc, cap, rid, tid)
        return redirect(url_for("classes.list_classes"))
    return render_template("edit_class.html", class_data=class_data, rooms=rooms, trainers=trainers)

@classes_bp.route("/delete/<int:cid>", methods=["POST"])
@login_required
def delete_class(cid):
    models.delete_fitness_class(cid)
    return redirect(url_for("classes.list_classes"))

@classes_bp.route("/schedule/add", methods=["GET", "POST"])
@login_required
def add_schedule():
    classes = models.get_all_classes()
    if request.method == "POST":
        class_id = request.form["ClassID"]
        date = request.form["ScheduleDate"]
        start = request.form["StartTime"]
        end = request.form["EndTime"]

        # Optional: validate inputs here
        try:
            models.create_class_schedule(class_id, date, start, end)
            flash("Class schedule added successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("classes.list_classes"))

    return render_template("add_schedule.html", classes=classes)

def get_schedule_by_id(sid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ClassSchedule WHERE ScheduleID = %s", (sid,))
    return cur.fetchone()

@classes_bp.route("/schedule/edit/<int:sid>", methods=["GET", "POST"])
@login_required
def edit_schedule(sid):
    sched = models.get_schedule_by_id(sid)
    classes = models.get_all_classes()

    if request.method == "POST":
        class_id = request.form["class_id"]
        date = request.form["schedule_date"]
        start = request.form["start_time"]
        end = request.form["end_time"]
        models.update_class_schedule(sid, class_id, date, start, end)
        return redirect(url_for("classes.list_classes"))

    return render_template("edit_schedule.html", sched=sched, classes=classes)

@classes_bp.route("/schedule/delete/<int:sid>", methods=["POST"])
@login_required
def delete_schedule(sid):
    models.delete_schedule(sid)
    return redirect(url_for("classes.list_classes"))

@classes_bp.route("/attendance/add", methods=["GET", "POST"])
@login_required
def add_attendance():
    members = models.get_all_members()
    schedules = models.get_all_class_schedules()
    if request.method == "POST":
        member_id = request.form["MemberID"]
        schedule_id = request.form["ScheduleID"]
        status = request.form.get("Status", "present")
        models.create_attendance(member_id, schedule_id, status)
        return redirect(url_for("classes.list_classes"))
    return render_template("add_attendance.html", members=members, schedules=schedules)

@classes_bp.route("/attendance/edit/<int:aid>", methods=["GET", "POST"])
@login_required
def edit_attendance(aid):
    attendance = models.get_attendance_by_id(aid)
    members = models.get_all_members()
    schedules = models.get_all_class_schedules()
    if request.method == "POST":
        member_id = request.form["MemberID"]
        schedule_id = request.form["ScheduleID"]
        status = request.form.get("Status", "present")
        models.update_attendance(aid, member_id, schedule_id, status)
        return redirect(url_for("classes.list_classes"))
    return render_template("edit_attendance.html", attendance=attendance, members=members, schedules=schedules)

@classes_bp.route("/attendance/delete/<int:aid>", methods=["POST"])
@login_required
def delete_attendance(aid):
    models.delete_attendance(aid)
    return redirect(url_for("classes.list_classes"))