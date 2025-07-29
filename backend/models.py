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
    db = get_db(); cur = db.cursor(dictionary=True)

    cur.execute("SELECT Role FROM `User` WHERE UserID=%s", (uid,))
    user = cur.fetchone()
    if not user:
        return

    if user["Role"] == "admin":
        cur.execute("SELECT COUNT(*) AS count FROM `User` WHERE Role='admin'")
        admin_count = cur.fetchone()["count"]
        if admin_count <= 1:
            raise Exception("Cannot delete the last admin user.")

    cur = db.cursor()
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
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            m.MemberID, m.FirstName, m.LastName, m.Email,
            m.MembershipStartDate,
            m.MembershipStatus,
            p.PlanName
        FROM Member m
        LEFT JOIN MembershipPlan p ON m.CurrentPlanID = p.PlanID
    """)
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

def update_member(
    mid, firstName, lastName, email,
    DateOfBirth=None, PhoneNumber=None,
    CurrentPlanID=None, MembershipStatus=None,
    MembershipStartDate=None
):
    db = get_db(); cur = db.cursor()
    cur.execute(
      """
      UPDATE Member SET 
        FirstName=%s, LastName=%s, Email=%s,
        DateOfBirth=%s, PhoneNumber=%s,
        CurrentPlanID=%s, MembershipStatus=%s, MembershipStartDate=%s
      WHERE MemberID=%s
      """,
      (
        firstName, lastName, email,
        DateOfBirth, PhoneNumber,
        CurrentPlanID, MembershipStatus,
        MembershipStartDate, mid
      )
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
def get_staff_by_id(sid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Staff WHERE StaffID=%s", (sid,))
    return cur.fetchone()

def update_staff(sid, FirstName, LastName, Email, Role):
    db = get_db(); cur = db.cursor()
    cur.execute(
      "UPDATE Staff SET FirstName=%s, LastName=%s, Email=%s, `Role`=%s WHERE StaffID=%s",
      (FirstName, LastName, Email, Role, sid)
    )
    db.commit()

def delete_staff(sid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Staff WHERE StaffID=%s", (sid,))
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

    # ── MaintenanceLog ──
def get_all_maintenance_logs():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MaintenanceLog")
    return cur.fetchall()

def get_maintenance_log_by_id(log_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MaintenanceLog WHERE LogID = %s", (log_id,))
    return cur.fetchone()

def create_maintenance_log(EquipmentID, ReportedBy, IssueDescription, ResolutionStatus='pending'):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        INSERT INTO MaintenanceLog (
            EquipmentID, ReportedBy, IssueDescription, ResolutionStatus
        ) VALUES (%s, %s, %s, %s)
    """, (EquipmentID, ReportedBy, IssueDescription, ResolutionStatus))
    db.commit()

def update_maintenance_resolution(log_id, ResolutionStatus, ResolutionNotes=None, ResolvedBy=None, ResolveDate=None):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        UPDATE MaintenanceLog
        SET ResolutionStatus = %s,
            ResolutionNotes = %s,
            ResolvedBy = %s,
            ResolveDate = %s
        WHERE LogID = %s
    """, (ResolutionStatus, ResolutionNotes, ResolvedBy, ResolveDate, log_id))
    db.commit()

    # ── CalendarEvent ──
def get_all_events():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM CalendarEvent")
    return cur.fetchall()

def get_event_by_id(event_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM CalendarEvent WHERE EventID = %s", (event_id,))
    return cur.fetchone()

def create_calendar_event(Title, StartTime, EndTime, CreatedBy, Description=None, Location=None, EventType='other'):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        INSERT INTO CalendarEvent (
            Title, Description, StartTime, EndTime,
            Location, CreatedBy, EventType
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (Title, Description, StartTime, EndTime, Location, CreatedBy, EventType))
    db.commit()

def delete_event(event_id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM CalendarEvent WHERE EventID = %s", (event_id,))
    db.commit()

def get_all_staff():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Staff")
    return cur.fetchall()

def create_staff(FirstName, LastName, Email, Role):
    db = get_db(); cur = db.cursor()
    cur.execute(
        "INSERT INTO Staff (FirstName, LastName, Email, Role) VALUES (%s, %s, %s, %s)",
        (FirstName, LastName, Email, Role)
    )
    db.commit()

def update_equipment(eid, EquipmentName, PurchaseDate, Condition, RoomID):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE Equipment SET EquipmentName=%s, PurchaseDate=%s, `Condition`=%s, RoomID=%s WHERE EquipmentID=%s",
        (EquipmentName, PurchaseDate, Condition, RoomID, eid)
    )
    db.commit()

def delete_equipment(eid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM Equipment WHERE EquipmentID=%s", (eid,))
    db.commit()

def get_equipment_by_id(eid):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Equipment WHERE EquipmentID = %s", (eid,))
    return cur.fetchone()

def get_class_by_id(cid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM FitnessClass WHERE ClassID=%s", (cid,))
    return cur.fetchone()

def update_fitness_class(cid, name, desc, capacity, room_id, trainer_id):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        UPDATE FitnessClass
        SET ClassName=%s, ClassDescription=%s, Capacity=%s,
            RoomID=%s, TrainerID=%s
        WHERE ClassID=%s
    """, (name, desc, capacity, room_id, trainer_id, cid))
    db.commit()

def delete_fitness_class(cid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM FitnessClass WHERE ClassID=%s", (cid,))
    db.commit()

def get_schedule_by_id(sid):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM ClassSchedule WHERE ScheduleID = %s", (sid,))
    return cur.fetchone()

def update_class_schedule(sid, class_id, date, start, end):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        UPDATE ClassSchedule
        SET ClassID = %s, ScheduleDate = %s, StartTime = %s, EndTime = %s
        WHERE ScheduleID = %s
    """, (class_id, date, start, end, sid))
    db.commit()

def delete_schedule(schedule_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM ClassSchedule WHERE ScheduleID = %s", (schedule_id,))
    conn.commit()
    cur.close()

def get_all_class_schedules():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM ClassSchedule")
    schedules = cur.fetchall()
    cur.close()
    return schedules

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

def get_attendance_by_id(attendance_id):
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Attendance WHERE AttendanceID = %s", (attendance_id,))
    return cur.fetchone()

def update_attendance(attendance_id, member_id, schedule_id, status):
    db = get_db(); cur = db.cursor()
    cur.execute("""
        UPDATE Attendance
        SET MemberID = %s, ScheduleID = %s, Status = %s
        WHERE AttendanceID = %s
    """, (member_id, schedule_id, status, attendance_id))
    db.commit()

def delete_attendance(attendance_id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Attendance WHERE AttendanceID = %s", (attendance_id,))
    db.commit()

def delete_maintenance_log(log_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM MaintenanceLog WHERE LogID = %s", (log_id,))
    db.commit()

def get_all_membership_plans():
    cursor.execute("SELECT * FROM MembershipPlan")
    return cursor.fetchall()

def get_all_membership_plans():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MembershipPlan")
    return cursor.fetchall()

def add_membership_plan(name, fee, level):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO MembershipPlan (PlanName, MonthlyFee, AccessLevel) VALUES (%s, %s, %s)",
        (name, fee, level)
    )
    db.commit()

def update_member_plan(member_id, plan_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE Member SET CurrentPlanID = %s, MembershipStartDate = CURDATE() WHERE MemberID = %s",
        (plan_id, member_id)
    )
    db.commit()

def record_membership_change(member_id, plan_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO MembershipHistory (MemberID, PlanID, StartDate) VALUES (%s, %s, CURDATE())",
        (member_id, plan_id)
    )
    db.commit()

def delete_plan(plan_id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM MembershipPlan WHERE PlanID = %s", (plan_id,))
    db.commit()

def add_membership_history(MemberID, PlanID, StartDate, EndDate=None):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO MembershipHistory (MemberID, PlanID, StartDate, EndDate) VALUES (%s, %s, %s, %s)",
        (MemberID, PlanID, StartDate, EndDate)
    )
    db.commit()

def get_membership_history(mid=None):
    db = get_db()
    cur = db.cursor(dictionary=True)

    if mid:
        cur.execute("""
            SELECT h.HistoryID, h.MemberID, m.FirstName, m.LastName,
                   h.PlanID, p.PlanName, h.StartDate, h.EndDate
            FROM MembershipHistory h
            JOIN Member m ON h.MemberID = m.MemberID
            JOIN MembershipPlan p ON h.PlanID = p.PlanID
            WHERE h.MemberID = %s
            ORDER BY h.StartDate DESC
        """, (mid,))
    else:
        cur.execute("""
            SELECT h.HistoryID, h.MemberID, m.FirstName, m.LastName,
                   h.PlanID, p.PlanName, h.StartDate, h.EndDate
            FROM MembershipHistory h
            JOIN Member m ON h.MemberID = m.MemberID
            JOIN MembershipPlan p ON h.PlanID = p.PlanID
            ORDER BY h.StartDate DESC
        """)

    return cur.fetchall()

def record_membership_change(member_id, plan_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO MembershipHistory (MemberID, PlanID, StartDate) VALUES (%s, %s, CURDATE())",
        (member_id, plan_id)
    )
    db.commit()

def delete_membership_history(history_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM MembershipHistory WHERE HistoryID = %s", (history_id,))
    db.commit()

def get_all_history():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MembershipHistory")
    return cur.fetchall()

def get_all_history():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM MembershipHistory")
    return cur.fetchall()

def get_membership_history_by_id(hid):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT h.*, p.PlanName, m.FirstName, m.LastName
        FROM MembershipHistory h
        JOIN MembershipPlan p ON h.PlanID = p.PlanID
        JOIN Member m ON h.MemberID = m.MemberID
        WHERE h.HistoryID = %s
    """, (hid,))
    return cursor.fetchone()

def get_member_id_by_history_id(hid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT MemberID FROM MembershipHistory WHERE HistoryID = %s", (hid,))
    row = cursor.fetchone()
    return row[0] if row else None

def delete_membership_plan(plan_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM MembershipPlan WHERE PlanID = %s", (plan_id,))
    db.commit()