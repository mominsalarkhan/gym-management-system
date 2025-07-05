from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import functools
import models

trainers_bp = Blueprint("trainers", __name__, url_prefix="/trainers")

def roles_required(*roles):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper

@trainers_bp.route("/")
@login_required
@roles_required("admin","manager")
def list_trainers():
    ts = models.get_all_trainers()
    return render_template("trainers.html", trainers=ts)

@trainers_bp.route("/add", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def add_trainer():
    if request.method == "POST":
        models.create_trainer(
          request.form["firstName"],
          request.form["lastName"],
          request.form["specialty"]
        )
        flash("Trainer added.", "success")
        return redirect(url_for("trainers.list_trainers"))
    return render_template("add_trainer.html")

@trainers_bp.route("/edit/<int:tid>", methods=["GET","POST"])
@login_required
@roles_required("admin","manager")
def edit_trainer(tid):
    if request.method == "POST":
        models.update_trainer(
          tid,
          request.form["firstName"],
          request.form["lastName"],
          request.form["specialty"]
        )
        flash("Trainer updated.", "success")
        return redirect(url_for("trainers.list_trainers"))
    t = models.get_trainer_by_id(tid)
    return render_template("edit_trainer.html", trainer=t)

@trainers_bp.route("/delete/<int:tid>", methods=["POST"])
@login_required
@roles_required("admin","manager")
def delete_trainer(tid):
    models.delete_trainer(tid)
    flash("Trainer deleted.", "warning")
    return redirect(url_for("trainers.list_trainers"))