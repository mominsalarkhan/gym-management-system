# 🏋️‍♀️ Gym Management System

## 📌 Final Project - Milestone 2

This is a Gym Management System developed for our **Database Systems** course project. The goal is to design a normalized relational database schema that models the core functionalities of a gym facility including membership management, class scheduling, trainer assignments, and equipment maintenance.

We use **PostgreSQL** as our database engine, and **[Supabase](https://supabase.com/)** to simplify deployment, hosting, and management of our database in the cloud.

---

## 📐 Database Schema

The schema is structured around real-world gym operations, with attention to **data normalization**, **referential integrity**, and **scalability**. Key design elements include:

* **UUIDs** as primary keys for all tables
* **Audit-friendly** historical tracking (e.g., `MembershipHistory`)
* **Many-to-many relationships** (e.g., members attending scheduled classes)
* **Cascade behavior** for foreign keys to maintain data consistency

<details>
<summary><strong>Click to view full SQL schema</strong></summary>

```sql
-- EXTENSION FOR UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* ---------- Core reference tables ---------- */
CREATE TABLE MembershipPlan (
    plan_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plan_name       VARCHAR(100) NOT NULL,
    monthly_fee     NUMERIC(10,2) NOT NULL CHECK (monthly_fee >= 0),
    access_level    VARCHAR(50) NOT NULL
);

CREATE TABLE Room (
    room_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_name   VARCHAR(100) NOT NULL UNIQUE,
    capacity    INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE Staff (
    staff_id    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name  VARCHAR(60) NOT NULL,
    last_name   VARCHAR(60) NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    role        VARCHAR(50) NOT NULL
);

/* ---------- Member-side tables ---------- */
CREATE TABLE Member (
    member_id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name             VARCHAR(60) NOT NULL,
    last_name              VARCHAR(60) NOT NULL,
    email                  VARCHAR(120) NOT NULL UNIQUE,
    phone_number           VARCHAR(20),
    date_of_birth          DATE,
    membership_start_date  DATE NOT NULL DEFAULT CURRENT_DATE,
    membership_status      VARCHAR(30) NOT NULL DEFAULT 'active',
    current_plan_id        UUID REFERENCES MembershipPlan(plan_id) ON UPDATE CASCADE
);

CREATE TABLE MembershipHistory (
    history_id  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    member_id   UUID NOT NULL REFERENCES Member(member_id) ON UPDATE CASCADE ON DELETE CASCADE,
    plan_id     UUID NOT NULL REFERENCES MembershipPlan(plan_id) ON UPDATE CASCADE,
    start_date  DATE NOT NULL,
    end_date    DATE,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE Payments (
    payment_id      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    member_id       UUID NOT NULL REFERENCES Member(member_id) ON UPDATE CASCADE ON DELETE CASCADE,
    amount          NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    payment_date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method  VARCHAR(30) NOT NULL,
    payment_status  VARCHAR(20) NOT NULL
);

/* ---------- Trainer + class tables ---------- */
CREATE TABLE Trainer (
    trainer_id  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name  VARCHAR(60) NOT NULL,
    last_name   VARCHAR(60) NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    specialty   VARCHAR(80)
);

CREATE TABLE FitnessClass (
    class_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_name       VARCHAR(80) NOT NULL,
    class_description TEXT,
    trainer_id       UUID NOT NULL REFERENCES Trainer(trainer_id) ON UPDATE CASCADE,
    room_id          UUID NOT NULL REFERENCES Room(room_id) ON UPDATE CASCADE,
    capacity         INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE ClassSchedule (
    schedule_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_id      UUID NOT NULL REFERENCES FitnessClass(class_id) ON UPDATE CASCADE ON DELETE CASCADE,
    schedule_date DATE NOT NULL,
    start_time    TIME NOT NULL,
    end_time      TIME NOT NULL,
    CHECK (end_time > start_time)
);

CREATE TABLE Attendance (
    attendance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    schedule_id   UUID NOT NULL REFERENCES ClassSchedule(schedule_id) ON UPDATE CASCADE ON DELETE CASCADE,
    member_id     UUID NOT NULL REFERENCES Member(member_id) ON UPDATE CASCADE ON DELETE CASCADE,
    status        VARCHAR(20) NOT NULL DEFAULT 'booked',
    UNIQUE (schedule_id, member_id)
);

/* ---------- Equipment & maintenance ---------- */
CREATE TABLE Equipment (
    equipment_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_name VARCHAR(100) NOT NULL,
    purchase_date  DATE,
    condition      VARCHAR(40) NOT NULL
);

CREATE TABLE EquipmentMaintenance (
    maintenance_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id           UUID NOT NULL REFERENCES Equipment(equipment_id) ON UPDATE CASCADE ON DELETE CASCADE,
    staff_id               UUID NOT NULL REFERENCES Staff(staff_id) ON UPDATE CASCADE,
    maintenance_date       DATE NOT NULL DEFAULT CURRENT_DATE,
    maintenance_description TEXT NOT NULL
);

/* ---------- Quick sanity indexes ---------- */
CREATE INDEX idx_attendance_member ON Attendance(member_id);
CREATE INDEX idx_schedule_class   ON ClassSchedule(class_id);
CREATE INDEX idx_member_email     ON Member(email);
```

</details>

---

## 🧑‍💻 Team

* Andre Joseph
* Arley Peter
* Momin Khan
* Richard Tairouz Aslam

---

## 📎 License

This project is for academic use only. Feel free to fork or adapt with attribution. Not intended for production environments. Please attribute credits and sources of our work.
