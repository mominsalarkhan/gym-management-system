# 🏋️‍♀️ Gym Management System

## 📌 Final Project - Milestone 2

This is a Gym Management System developed for our **Database Systems** course project. The goal is to design a normalized relational database schema that models the core functionalities of a gym facility including membership management, class scheduling, trainer assignments, and equipment maintenance.

We use **MySQL** as our database engine with automatic database initialization for easy setup and deployment.

---

## 📐 Database Schema

The schema is structured around real-world gym operations, with attention to **data normalization**, **referential integrity**, and **scalability**. Key design elements include:

* **Auto-incrementing integers** as primary keys for all tables
* **Audit-friendly** historical tracking (e.g., `MembershipHistory`)
* **Many-to-many relationships** (e.g., members attending scheduled classes)
* **Cascade behavior** for foreign keys to maintain data consistency
* **Automatic database initialization** with sample data

<details>
<summary><strong>Click to view full MySQL schema</strong></summary>

```sql
-- MySQL Database Schema for Gym Management System

CREATE DATABASE IF NOT EXISTS gymdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gymdb;

SET FOREIGN_KEY_CHECKS=0;

/* ---------- Core reference tables ---------- */
CREATE TABLE IF NOT EXISTS MembershipPlan (
    PlanID       INT            AUTO_INCREMENT PRIMARY KEY,
    PlanName     VARCHAR(50)    NOT NULL,
    MonthlyFee   DECIMAL(8,2)   NOT NULL,
    AccessLevel  VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Room (
    RoomID    INT AUTO_INCREMENT PRIMARY KEY,
    RoomName  VARCHAR(50)  NOT NULL,
    Capacity  INT          NOT NULL
);

CREATE TABLE IF NOT EXISTS Staff (
    StaffID   INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName  VARCHAR(50) NOT NULL,
    Email     VARCHAR(100) NOT NULL UNIQUE,
    `Role`    VARCHAR(50)
);

/* ---------- Member-side tables ---------- */
CREATE TABLE IF NOT EXISTS Member (
    MemberID             INT             AUTO_INCREMENT PRIMARY KEY,
    FirstName            VARCHAR(50)     NOT NULL,
    LastName             VARCHAR(50)     NOT NULL,
    Email                VARCHAR(100)    NOT NULL UNIQUE,
    DateOfBirth          DATE,
    PhoneNumber          VARCHAR(20),
    CurrentPlanID        INT,
    MembershipStatus     VARCHAR(20),
    MembershipStartDate  DATE,
    FOREIGN KEY (CurrentPlanID)
        REFERENCES MembershipPlan(PlanID)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS MembershipHistory (
    HistoryID  INT AUTO_INCREMENT PRIMARY KEY,
    MemberID   INT NOT NULL,
    PlanID     INT NOT NULL,
    StartDate  DATE NOT NULL,
    EndDate    DATE,
    FOREIGN KEY (MemberID)
        REFERENCES Member(MemberID)
        ON DELETE CASCADE,
    FOREIGN KEY (PlanID)
        REFERENCES MembershipPlan(PlanID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Payments (
    PaymentID     INT AUTO_INCREMENT PRIMARY KEY,
    MemberID      INT NOT NULL,
    Amount        DECIMAL(10,2) NOT NULL,
    PaymentDate   DATE NOT NULL,
    PaymentMethod VARCHAR(50),
    PaymentStatus VARCHAR(20),
    FOREIGN KEY (MemberID)
        REFERENCES Member(MemberID) ON DELETE CASCADE
);

/* ---------- Trainer + class tables ---------- */
CREATE TABLE IF NOT EXISTS Trainer (
    TrainerID  INT AUTO_INCREMENT PRIMARY KEY,
    FirstName  VARCHAR(50) NOT NULL,
    LastName   VARCHAR(50) NOT NULL,
    Email      VARCHAR(100) NOT NULL UNIQUE,
    Specialty  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS FitnessClass (
    ClassID         INT AUTO_INCREMENT PRIMARY KEY,
    ClassName       VARCHAR(50) NOT NULL,
    ClassDescription TEXT,
    Capacity        INT NOT NULL,
    RoomID          INT NOT NULL,
    TrainerID       INT NOT NULL,
    FOREIGN KEY (RoomID)
        REFERENCES Room(RoomID) ON DELETE RESTRICT,
    FOREIGN KEY (TrainerID)
        REFERENCES Trainer(TrainerID) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ClassSchedule (
    ScheduleID   INT AUTO_INCREMENT PRIMARY KEY,
    ClassID      INT NOT NULL,
    ScheduleDate DATE NOT NULL,
    StartTime    TIME NOT NULL,
    EndTime      TIME NOT NULL,
    FOREIGN KEY (ClassID)
        REFERENCES FitnessClass(ClassID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Attendance (
    AttendanceID INT AUTO_INCREMENT PRIMARY KEY,
    MemberID     INT NOT NULL,
    ScheduleID   INT NOT NULL,
    Status       VARCHAR(20),
    FOREIGN KEY (MemberID)
        REFERENCES Member(MemberID) ON DELETE CASCADE,
    FOREIGN KEY (ScheduleID)
        REFERENCES ClassSchedule(ScheduleID) ON DELETE CASCADE
);

/* ---------- Equipment & maintenance ---------- */
CREATE TABLE IF NOT EXISTS Equipment (
    EquipmentID    INT AUTO_INCREMENT PRIMARY KEY,
    EquipmentName  VARCHAR(50) NOT NULL,
    PurchaseDate   DATE,
    `Condition`    VARCHAR(50),
    RoomID         INT,
    FOREIGN KEY (RoomID)
        REFERENCES Room(RoomID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS EquipmentMaintenance (
    MaintenanceID         INT AUTO_INCREMENT PRIMARY KEY,
    EquipmentID           INT NOT NULL,
    StaffID               INT NOT NULL,
    MaintenanceDescription TEXT,
    MaintenanceDate       DATE NOT NULL,
    FOREIGN KEY (EquipmentID)
        REFERENCES Equipment(EquipmentID) ON DELETE CASCADE,
    FOREIGN KEY (StaffID)
        REFERENCES Staff(StaffID) ON DELETE CASCADE
);

/* ---------- User authentication ---------- */
CREATE TABLE IF NOT EXISTS `User` (
    UserID       INT             AUTO_INCREMENT PRIMARY KEY,
    Username     VARCHAR(50)     NOT NULL UNIQUE,
    PasswordHash VARCHAR(128)    NOT NULL,
    Role         ENUM('admin','manager','trainer','member') NOT NULL
);

SET FOREIGN_KEY_CHECKS=1;
```

</details>

---

## 🚀 Getting Started

### Prerequisites

- **MySQL Server** (version 5.7 or higher)
- **Python** (version 3.8 or higher)
- **pip** (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gym-management-system
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   # or if using uv
   uv sync
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_USER=root
   DB_PASS=your_mysql_password
   DB_NAME=gymdb
   
   # Application Configuration
   SECRET_KEY=your-secret-key-here-change-this-in-production
   
   # Admin User Configuration
   ADMIN_USER=admin
   ADMIN_PASS=admin
   ```

4. **Initialize the database**
   
   **Option 1: Using the setup script (Recommended)**
   ```bash
   python setup_database.py
   ```
   
   **Option 2: Automatic initialization**
   ```bash
   python app.py
   ```
   The database will be created automatically when you first run the application.

5. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5001`
   
   **Default login credentials:**
   - Username: `admin`
   - Password: `admin`

### Features

- **🔧 Automatic Database Setup**: No manual SQL scripts needed
- **👥 User Management**: Admin, manager, trainer, and member roles
- **💳 Membership Plans**: Flexible membership plan management
- **🏃‍♂️ Member Management**: Complete member profile and history tracking
- **👨‍🏫 Trainer Management**: Trainer profiles and specialties
- **🏢 Room Management**: Gym facility and room management
- **📅 Class Scheduling**: Fitness class scheduling and management
- **📊 Attendance Tracking**: Member attendance for classes
- **💰 Payment Processing**: Payment history and status tracking
- **🔧 Equipment Management**: Equipment inventory and maintenance
- **📈 Reporting**: Various reports and analytics

### Database Features

- **Automatic Initialization**: Database and tables created automatically
- **Sample Data**: Includes sample membership plans and rooms
- **Data Integrity**: Foreign key constraints and referential integrity
- **Normalized Schema**: Properly normalized database design
- **Audit Trail**: Historical tracking for memberships and payments

---

## 🧑‍💻 Team

* Andre Joseph
* Arley Peter
* Momin Khan
* Richard Tairouz Aslam

---

## 📎 License

This project is for academic use only. Feel free to fork or adapt with attribution. Not intended for production environments. Please attribute credits and sources of our work.
