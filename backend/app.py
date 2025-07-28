import os
from dotenv import load_dotenv
load_dotenv()
from models import get_user_by_id, User

from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash

import models
import auth
import members
import membership
import trainers
import rooms
import users
import equipment
import api
import db_init
import maintenance
import class_calendar
import admin
import classes
import staff

# ── Flask App Setup ──
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../frontend"),
    static_url_path=""
)
app.config.from_prefixed_env()
app.secret_key = os.getenv("SECRET_KEY")

# ── Flask-Login Setup ──
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# ── Ensure Database and Admin ──
def ensure_database_and_admin():
    try:
        if not db_init.check_database_exists():
            print("Database not found. Initializing database...")
            db_init.initialize_database()

        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_pass = os.getenv("ADMIN_PASS", "admin")

        if not models.get_user_by_username(admin_user):
            pw_hash = generate_password_hash(admin_pass, method="pbkdf2:sha256")
            db = models.get_db()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO `User` (Username, PasswordHash, Role) VALUES (%s, %s, %s)",
                (admin_user, pw_hash, "admin")
            )
            db.commit()
            print(f"Default admin user '{admin_user}' created successfully!")

    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise

# ── Register Blueprints ──
app.register_blueprint(auth.auth_bp)
app.register_blueprint(users.users_bp)
app.register_blueprint(members.members_bp)
app.register_blueprint(membership.membership_bp)
app.register_blueprint(trainers.trainers_bp)
app.register_blueprint(rooms.rooms_bp)
app.register_blueprint(equipment.equipment_bp)
app.register_blueprint(api.api)
app.register_blueprint(maintenance.maintenance_bp)
app.register_blueprint(class_calendar.calendar_bp)
app.register_blueprint(admin.admin_bp)
app.register_blueprint(classes.classes_bp)
app.register_blueprint(staff.staff_bp)

# ── Routes ──
@app.route("/")
def index():
    return redirect(url_for("dashboard")) if current_user.is_authenticated else redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ── Entry Point ──
if __name__ == "__main__":
    ensure_database_and_admin()
    app.run(port=5001, debug=True)