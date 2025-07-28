
# Database Setup Guide

This guide explains how to set up the database for the Gym Management System.

---

## 🚀 Automatic Database Initialization

The system includes automatic database setup that will:

- Create the database if it doesn't exist
- Create all required tables
- Insert sample data into:
  - Membership Plans
  - Rooms
  - Trainers
  - Members
  - Fitness Classes and Schedules
  - Payments
  - Attendance
  - Equipment
  - Staff
  - Equipment Maintenance
  - Membership History
- Set up a default admin user

---

## ⚙️ Setup Methods

### ✅ Method 1: Using the Setup Script (Recommended)

Run the setup script manually if you want full control:

```bash
python setup_database.py
```

The script will:

- Check if the database exists
- Create the database and tables if needed
- Insert sample data
- Show the default admin login credentials

---

### 🔄 Method 2: Automatic Setup on App Launch

If you don’t want to run the script manually, the app will auto-initialize:

```bash
python app.py
```

If the database doesn’t exist, it will be created along with all required tables and sample data.

---

## 🔐 Environment Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASS=your_database_password
DB_NAME=gymdb

# Application Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# Admin User Configuration
ADMIN_USER=admin
ADMIN_PASS=admin
```

---

## 🧱 Database Schema

The system automatically creates the following tables:

### Core Tables
- `User` — System users (admin, manager, trainer, member)
- `MembershipPlan` — Membership tiers
- `Member` — Registered gym members
- `Trainer` — Trainers available at the gym
- `Room` — Rooms and facilities

### Operational Tables
- `MembershipHistory` — Membership changes and upgrades
- `FitnessClass` — Types of classes
- `ClassSchedule` — Scheduled class times
- `Attendance` — Who attended which class
- `Payments` — Member payments
- `Equipment` — Equipment inventory
- `Staff` — Non-trainer staff (e.g. maintenance)
- `EquipmentMaintenance` — Maintenance activity logs
- `MaintenanceLog` — Reported/resolved issues
- `CalendarEvent` — General-purpose event calendar

---

## 📦 Sample Data Included

### Membership Plans
- Basic Plan — $29.99/month
- Standard Plan — $49.99/month
- Premium Plan — $79.99/month
- VIP Plan — $129.99/month

### Rooms
- Main Gym — 50 capacity
- Cardio Room — 30 capacity
- Yoga Studio — 20 capacity
- Spin Class Room — 25 capacity
- Weight Room — 40 capacity

### Trainers
- John Doe — Strength
- Jane Smith — Yoga
- Mike Johnson — Cardio

### Members
- Alice Smith
- Bob Brown
- Charlie Davis

### Classes
- Yoga Flow — Yoga Studio, Jane Smith
- HIIT — Main Gym, John Doe

### Schedules
- Yoga Flow: Daily 9:00–10:00 AM
- HIIT: Every Mon/Wed/Fri 6:00–7:00 PM

### Attendance
- Sample attendance records for Alice and Bob

### Payments
- Recent payments made by each sample member

### Equipment
- Treadmills, Dumbbells, Mats, etc.

### Staff
- Maintenance and support staff

### Equipment Maintenance
- Example records of past maintenance

### Membership History
- History records for Alice and Bob showing plan changes and durations

---

## 👤 Default Admin Account

After setup, log in with:

- **Username:** `admin` (or `ADMIN_USER` from `.env`)
- **Password:** `admin` (or `ADMIN_PASS` from `.env`)

You can change these in your `.env` file or reset via the database.

---

## 🧹 Manual Database Reset

If you want to reset everything:

1. Run:
   ```bash
   python setup_database.py
   ```
2. When prompted, choose `y` to reinitialize the database.

---

## 🛠 Troubleshooting

### Database Connection Issues

- ✅ Ensure MySQL server is running
- ✅ Verify credentials in `.env`
- ✅ Confirm your DB user has permission to create databases

### Permissions Required

Your MySQL user needs:
- `CREATE`, `DROP`
- `INSERT`, `UPDATE`, `DELETE`
- `SELECT`, `REFERENCES`

---

## ✅ Features

- Automatic database detection
- Safe `IF NOT EXISTS` table creation
- Rich sample data across all tables
- Modular and reusable setup logic
- Environment-based configuration
- Error logging with helpful messages