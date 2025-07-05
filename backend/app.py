import os
from dotenv import load_dotenv
load_dotenv()  

from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash

import models
import auth
import members
import trainers
import rooms
import users
import equipment
import api
import db_init

# Point Flask at sibling frontend/ for static files
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../frontend"),
    static_url_path=""
)
# Now these will pick up from .env
app.config.from_prefixed_env()

app.secret_key = os.getenv("SECRET_KEY")

# ── Flask-Login setup ──
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return models.get_user_by_id(user_id)

def ensure_database_and_admin():
    """
    Initialize database and create the default admin user if it doesn't already exist.
    Uses ADMIN_USER and ADMIN_PASS from environment.
    """
    try:
        # Initialize database if it doesn't exist
        if not db_init.check_database_exists():
            print("Database not found. Initializing database...")
            db_init.initialize_database()
        
        # Create default admin user
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

# Register your blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(users.users_bp)
app.register_blueprint(members.members_bp)
app.register_blueprint(trainers.trainers_bp)
app.register_blueprint(rooms.rooms_bp)
app.register_blueprint(equipment.equipment_bp)
app.register_blueprint(api.api)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dashboard.html")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    ensure_database_and_admin()
    app.run(port=5001, debug=True)