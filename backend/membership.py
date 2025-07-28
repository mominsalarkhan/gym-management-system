from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import (
    get_all_membership_plans, add_membership_plan, delete_membership_plan,
    get_membership_history, add_membership_history,
    get_all_members,  
)

membership_bp = Blueprint("membership", __name__, template_folder="templates")

@membership_bp.route("/plans")
def view_plans():
    plans = get_all_membership_plans()
    return render_template("membership_plans.html", plans=plans)

@membership_bp.route("/plans/add", methods=["GET", "POST"])
def add_plan():
    if request.method == "POST":
        add_membership_plan(
            request.form["PlanName"],
            request.form["MonthlyFee"],
            request.form.get("AccessLevel", "")
        )
        flash("Plan added successfully", "success")
        return redirect(url_for("membership.view_plans"))
    return render_template("add_plan.html")

@membership_bp.route("/plans/delete/<int:plan_id>", methods=["POST"])
def delete_plan(plan_id):
    delete_membership_plan(plan_id)
    flash("Plan deleted", "info")
    return redirect(url_for("membership.view_plans"))

@membership_bp.route("/history")
def view_history():
    history = get_membership_history()
    return render_template("membership_history.html", history=history)

@membership_bp.route("/history/add", methods=["GET", "POST"])
def add_history():
    if request.method == "POST":
        add_membership_history(
            request.form["MemberID"],
            request.form["PlanID"],
            request.form["StartDate"],
            request.form.get("EndDate")
        )
        flash("History record added", "success")
        return redirect(url_for("membership.view_history"))
    members = get_all_members()
    plans = get_all_membership_plans()
    return render_template("add_history.html", members=members, plans=plans)