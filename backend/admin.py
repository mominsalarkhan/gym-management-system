# admin.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import models

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403

    user_count = len(models.get_all_users())
    member_count = len(models.get_all_members())
    trainer_count = len(models.get_all_trainers())
    equipment_count = len(models.get_all_equipment())
    payment_count = len(models.get_all_payments())

    return render_template(
        "admin_dashboard.html",
        user_count=user_count,
        member_count=member_count,
        trainer_count=trainer_count,
        equipment_count=equipment_count,
        payment_count=payment_count
    )
