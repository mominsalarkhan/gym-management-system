import os
import mysql.connector
from flask_login import UserMixin

from werkzeug.security import generate_password_hash

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "gymdb")
    )

# ── User Model ──
class User(UserMixin):
    def __init__(self, uid, username, password_hash, role):
        self.id = uid
        self.Username = username
        self.PasswordHash = password_hash
        self.Role = role

    @property
    def role(self):
        return self.Role

def create_user(username, raw_password, role="member"):
    pw_hash = generate_password_hash(raw_password, method="pbkdf2:sha256")
    db = get_db(); cur = db.cursor()
    cur.execute(
        "INSERT INTO `User` (Username, PasswordHash, Role) VALUES (%s, %s, %s)",
        (username, pw_hash, role)
    )
    db.commit()
    
def get_user_by_username(username):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM `User` WHERE Username=%s", (username,))
    row = cur.fetchone()
    return None if not row else User(row["UserID"], row["Username"], row["PasswordHash"], row["Role"])

def get_user_by_id(uid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM `User` WHERE UserID=%s", (uid,))
    row = cur.fetchone()
    return None if not row else User(row["UserID"], row["Username"], row["PasswordHash"], row["Role"])

def get_all_users():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM `User`")
    return cur.fetchall()

def update_user(uid, username, role):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "UPDATE `User` SET Username=%s, Role=%s WHERE UserID=%s",
      (username, role, uid)
    )
    db.commit()

def delete_user(uid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM `User` WHERE UserID=%s", (uid,))
    db.commit()

# ── MembershipPlan ──
def get_all_plans():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MembershipPlan")
    return cur.fetchall()

def create_plan(planName, monthlyFee, accessLevel=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO MembershipPlan (PlanName, MonthlyFee, AccessLevel) VALUES (%s,%s,%s)",
      (planName, monthlyFee, accessLevel)
    )
    db.commit()

# ── Member ──
def get_all_members():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Member")
    return cur.fetchall()

def get_member_by_id(mid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Member WHERE MemberID=%s", (mid,))
    return cur.fetchone()

def create_member(
    firstName, lastName, email,
    DateOfBirth=None, PhoneNumber=None,
    CurrentPlanID=None, MembershipStatus=None,
    MembershipStartDate=None
):
    db = get_db(); cur = db.cursor()
    cur.execute(
      """
      INSERT INTO Member (
        FirstName, LastName, Email,
        DateOfBirth, PhoneNumber,
        CurrentPlanID, MembershipStatus, MembershipStartDate
      ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
      """,
      (
        firstName, lastName, email,
        DateOfBirth, PhoneNumber,
        CurrentPlanID, MembershipStatus,
        MembershipStartDate
      )
    )
    db.commit()

def update_member(mid, firstName, lastName, email):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "UPDATE Member SET FirstName=%s, LastName=%s, Email=%s WHERE MemberID=%s",
      (firstName, lastName, email, mid)
    )
    db.commit()

def delete_member(mid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Member WHERE MemberID=%s", (mid,))
    db.commit()

# ── MembershipHistory ──
def get_all_history():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MembershipHistory")
    return cur.fetchall()

def create_membership_history(MemberID, PlanID, StartDate, EndDate=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO MembershipHistory (MemberID, PlanID, StartDate, EndDate) VALUES (%s,%s,%s,%s)",
      (MemberID, PlanID, StartDate, EndDate)
    )
    db.commit()

# ── Trainer ──
def get_all_trainers():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Trainer")
    return cur.fetchall()

def get_trainer_by_id(tid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Trainer WHERE TrainerID=%s", (tid,))
    return cur.fetchone()

def create_trainer(FirstName, LastName, Email, Specialty=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO Trainer (FirstName, LastName, Email, Specialty) VALUES (%s,%s,%s,%s)",
      (FirstName, LastName, Email, Specialty)
    )
    db.commit()

def update_trainer(tid, FirstName, LastName, Specialty):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "UPDATE Trainer SET FirstName=%s, LastName=%s, Specialty=%s WHERE TrainerID=%s",
      (FirstName, LastName, Specialty, tid)
    )
    db.commit()

def delete_trainer(tid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Trainer WHERE TrainerID=%s", (tid,))
    db.commit()

# ── Room ──
def get_all_rooms():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Room")
    return cur.fetchall()

def get_room_by_id(rid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Room WHERE RoomID=%s", (rid,))
    return cur.fetchone()

def create_room(RoomName, Capacity):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO Room (RoomName, Capacity) VALUES (%s,%s)",
      (RoomName, Capacity)
    )
    db.commit()

def update_room(rid, RoomName, Capacity):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "UPDATE Room SET RoomName=%s, Capacity=%s WHERE RoomID=%s",
      (RoomName, Capacity, rid)
    )
    db.commit()

def delete_room(rid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Room WHERE RoomID=%s", (rid,))
    db.commit()

# ── FitnessClass ──
def get_all_classes():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM FitnessClass")
    return cur.fetchall()

def create_fitness_class(ClassName, Capacity, RoomID, TrainerID, ClassDescription=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      """
      INSERT INTO FitnessClass (
        ClassName, ClassDescription,
        Capacity, RoomID, TrainerID
      ) VALUES (%s,%s,%s,%s,%s)
      """,
      (ClassName, ClassDescription, Capacity, RoomID, TrainerID)
    )
    db.commit()

# ── ClassSchedule ──
def get_all_schedules():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ClassSchedule")
    return cur.fetchall()

def create_class_schedule(ClassID, ScheduleDate, StartTime, EndTime):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO ClassSchedule (ClassID, ScheduleDate, StartTime, EndTime) VALUES (%s,%s,%s,%s)",
      (ClassID, ScheduleDate, StartTime, EndTime)
    )
    db.commit()

# ── Attendance ──
def get_all_attendance():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Attendance")
    return cur.fetchall()

def create_attendance(MemberID, ScheduleID, Status=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO Attendance (MemberID, ScheduleID, Status) VALUES (%s,%s,%s)",
      (MemberID, ScheduleID, Status)
    )
    db.commit()

# ── Payments ──
def get_all_payments():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Payments")
    return cur.fetchall()

def create_payment(MemberID, Amount, PaymentDate, PaymentMethod=None, PaymentStatus=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      """
      INSERT INTO Payments (
        MemberID, Amount, PaymentDate,
        PaymentMethod, PaymentStatus
      ) VALUES (%s,%s,%s,%s,%s)
      """,
      (MemberID, Amount, PaymentDate, PaymentMethod, PaymentStatus)
    )
    db.commit()

# ── Equipment ──
def get_all_equipment():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Equipment")
    return cur.fetchall()

def create_equipment(EquipmentName, PurchaseDate=None, Condition=None, RoomID=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO Equipment (EquipmentName, PurchaseDate, `Condition`, RoomID) VALUES (%s,%s,%s,%s)",
      (EquipmentName, PurchaseDate, Condition, RoomID)
    )
    db.commit()

# ── Staff ──
def get_all_staff():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Staff")
    return cur.fetchall()

def create_staff(FirstName, LastName, Email, Role=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "INSERT INTO Staff (FirstName, LastName, Email, `Role`) VALUES (%s,%s,%s,%s)",
      (FirstName, LastName, Email, Role)
    )
    db.commit()

# ── EquipmentMaintenance ──
def get_all_maintenance():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM EquipmentMaintenance")
    return cur.fetchall()

def create_equipment_maintenance(EquipmentID, StaffID, MaintenanceDate, MaintenanceDescription=None):
    db = get_db(); cur = db.cursor()
    cur.execute(
      """
      INSERT INTO EquipmentMaintenance (
        EquipmentID, StaffID,
        MaintenanceDate, MaintenanceDescription
      ) VALUES (%s,%s,%s,%s)
      """,
      (EquipmentID, StaffID, MaintenanceDate, MaintenanceDescription)
    )
    db.commit()