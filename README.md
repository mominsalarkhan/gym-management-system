# 🏋️‍♀️ Gym Management System

## 📌 Final Project - Milestone 2

This is a Gym Management System developed for our **Database Systems** course project. The goal is to design a normalized relational database schema that models the core functionalities of a gym facility including membership management, class scheduling, trainer assignments, and equipment maintenance.

We use **MySQL** as our database engine with automatic database initialization for easy setup and deployment.

---

## 📐 Database Schema

The schema is structured around real-world gym operations, with attention to **data normalization**, **referential integrity**, and **scalability**. Key design elements include:

* Auto-incrementing integers as primary keys for all tables
* Audit-friendly historical tracking (e.g., `MembershipHistory`)
* Many-to-many relationships (e.g., members attending scheduled classes)
* Cascade behavior for foreign keys to maintain data consistency
* Automatic database initialization with sample data

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
   ```

3. **Configure environment variables**

   Create a `.env` file in the `backend` directory:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASS=your_mysql_password
   DB_NAME=gymdb
   SECRET_KEY=your-secret-key
   ADMIN_USER=admin
   ADMIN_PASS=admin
   ```

4. **Initialize the database**
   ```bash
   python app.py
   ```

5. **Access the application**
   Navigate to: `http://localhost:5001`

---

## ✨ Features

- 🔐 User authentication & role-based access
- 👥 User account management (admin/manager/trainer/member)
- 🧾 Membership plans and membership history
- 📆 Class scheduling and trainer assignment
- 🏃 Member attendance tracking
- 🏢 Room management
- 💳 Payment recording
- 🛠️ Equipment tracking and maintenance
- 📊 Admin dashboard and management views
- 💡 Error handling and access control

---

## 🧑‍💻 Team

* Andre Joseph
* Arley Peter
* Momin Khan
* Richard Tairouz Aslam

---

## 📎 License

For academic use only.