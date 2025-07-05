from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    membership_id = db.Column(db.Integer, db.ForeignKey('membership_plan.id'))
    membership_history = db.relationship('MembershipPlanHistory', backref='user', lazy=True)

class MembershipPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_months = db.Column(db.Integer)
    price = db.Column(db.Float)
    users = db.relationship('User', backref='membership', lazy=True)

class MembershipPlanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan_name = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class ClassAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    class_name = db.Column(db.String(100))
    date = db.Column(db.Date)

class ClassCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer = db.Column(db.String(100))
    class_name = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

class EquipmentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100))
    status = db.Column(db.String(100))
    last_maintenance_date = db.Column(db.Date)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/assign_membership', methods=['GET', 'POST'])
def assign_membership():
    if request.method == 'POST':
        user = User.query.get(int(request.form['user_id']))
        plan = MembershipPlan.query.get(int(request.form['plan_id']))
        user.membership = plan
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=plan.duration_months*30)
        history = MembershipPlanHistory(user_id=user.id, plan_name=plan.name, start_date=start_date, end_date=end_date)
        db.session.add(history)
        db.session.commit()
        flash("Membership assigned.")
        return redirect(url_for('index'))
    users = User.query.all()
    plans = MembershipPlan.query.all()
    return render_template('assign_membership.html', users=users, plans=plans)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        class_name = request.form['class_name']
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        record = ClassAttendance(user_id=user_id, class_name=class_name, date=date)
        db.session.add(record)
        db.session.commit()
        flash("Attendance logged.")
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('attendance.html', users=users)

@app.route('/calendar')
def calendar():
    classes = ClassCalendar.query.order_by(ClassCalendar.date, ClassCalendar.time).all()
    return render_template('calendar.html', classes=classes)

@app.route('/equipment', methods=['GET', 'POST'])
def equipment():
    if request.method == 'POST':
        equipment_name = request.form['equipment_name']
        status = request.form['status']
        last_maintenance_date = datetime.datetime.strptime(request.form['last_maintenance_date'], '%Y-%m-%d').date()
        log = EquipmentLog(equipment_name=equipment_name, status=status, last_maintenance_date=last_maintenance_date)
        db.session.add(log)
        db.session.commit()
        flash("Equipment updated.")
        return redirect(url_for('equipment'))
    logs = EquipmentLog.query.all()
    return render_template('equipment.html', logs=logs)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        new_password = generate_password_hash(request.form['new_password'])
        user.password = new_password
        db.session.commit()
        flash('Password changed.')
        return redirect(url_for('index'))
    return render_template('change_password.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)