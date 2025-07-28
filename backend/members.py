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
@roles_required("admin", "manager", "trainer")
def list_members():
    ms = models.get_all_members()
    return render_template("members.html", members=ms)

@members_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def add_member():
    plans = models.get_all_membership_plans()

    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        dob = request.form.get("dateOfBirth") or None
        phone = request.form.get("phoneNumber") or None
        current_plan_id = request.form.get("currentPlanID") or None
        membership_status = request.form.get("membershipStatus") or "active"
        start_date = request.form.get("membershipStartDate") or None

        models.create_member(
            first_name,
            last_name,
            email,
            dob,
            phone,
            current_plan_id,
            membership_status,
            start_date
        )
        flash("Member added.", "success")
        return redirect(url_for("members.list_members"))

    return render_template("add_member.html", plans=plans)

@members_bp.route("/edit/<int:mid>", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def edit_member(mid):
    member = models.get_member_by_id(mid)
    plans = models.get_all_membership_plans()

    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        dob = request.form.get("dateOfBirth") or None
        phone = request.form.get("phoneNumber") or None
        current_plan_id = request.form.get("currentPlanID") or None
        membership_status = request.form.get("membershipStatus") or "active"
        start_date = request.form.get("membershipStartDate") or None

        models.update_member(
            mid,
            first_name,
            last_name,
            email,
            dob,
            phone,
            current_plan_id,
            membership_status,
            start_date
        )
        flash("Member updated.", "success")
        return redirect(url_for("members.list_members"))

    return render_template("edit_member.html", member=member, plans=plans)

@members_bp.route("/delete/<int:mid>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def delete_member(mid):
    models.delete_member(mid)
    flash("Member deleted.", "warning")
    return redirect(url_for("members.list_members"))

@members_bp.route("/history/<int:mid>")
@login_required
@roles_required("admin", "manager")
def view_membership_history(mid):
    history = models.get_membership_history(mid)
    member = models.get_member_by_id(mid)
    return render_template("membership_history.html", history=history, member=member)

@members_bp.route("/history/add", defaults={"mid": None}, methods=["GET", "POST"])
@members_bp.route("/history/add/<int:mid>", methods=["GET", "POST"])
@login_required
def add_membership_history(mid):
    member = models.get_member_by_id(mid) if mid else None

    if request.method == "POST":
        plan_id = request.form["plan_id"]
        start_date = request.form["start_date"]
        end_date = request.form.get("end_date") or None

        mid = int(request.form.get("MemberID", 0))

        models.add_membership_history(mid, plan_id, start_date, end_date)
        flash("History added.", "success")
        return redirect(url_for("membership.view_history"))

    plans = models.get_all_membership_plans()
    members = models.get_all_members()
    return render_template("add_membership_history.html", member=member, plans=plans, members=members)

@members_bp.route("/plans/add", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def add_membership_plan():
    if request.method == "POST":
        name = request.form["PlanName"]
        fee = request.form["MonthlyFee"]
        level = request.form.get("AccessLevel")

        models.add_membership_plan(name, fee, level)
        flash("Membership plan added.", "success")
        return redirect(url_for("members.list_membership_plans"))

    return render_template("add_membership_plan.html")

@members_bp.route("/plans/delete/<int:pid>", methods=["POST"])
@login_required
@roles_required("admin")
def delete_membership_plan(pid):
    models.delete_plan(pid)
    flash("Membership plan deleted.", "warning")
    return redirect(url_for("members.list_membership_plans"))

@members_bp.route("/plans")
@login_required
@roles_required("admin", "manager")
def list_membership_plans():
    plans = models.get_all_membership_plans()
    return render_template("membership_plans.html", plans=plans)

@members_bp.route("/history/edit/<int:hid>", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def edit_membership_history(hid):
    history = models.get_membership_history_by_id(hid)
    plans = models.get_all_membership_plans()
    if request.method == "POST":
        plan_id = request.form["PlanID"]
        start_date = request.form["StartDate"]
        end_date = request.form.get("EndDate") or None
        models.update_membership_history(hid, plan_id, start_date, end_date)
        flash("Membership history updated.", "success")
        return redirect(url_for("members.view_membership_history", mid=history["MemberID"]))
    return render_template("edit_membership_history.html", history=history, plans=plans)

@members_bp.route("/history/delete/<int:hid>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def delete_membership_history(hid):
    member_id = models.get_member_id_by_history_id(hid)
    models.delete_membership_history(hid)
    flash("Membership history deleted.", "warning")
    return redirect(url_for("members.view_membership_history", mid=member_id))