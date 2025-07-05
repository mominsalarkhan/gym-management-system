# Database Setup Guide

This guide explains how to set up the database for the Gym Management System.

## Automatic Database Initialization

The system now includes automatic database initialization that will:
- Create the database if it doesn't exist
- Create all required tables
- Insert sample data (membership plans and rooms)
- Set up the default admin user

## Setup Methods

### Method 1: Using the Setup Script (Recommended)

1. Run the database setup script:
   ```bash
   python setup_database.py
   ```

2. The script will:
   - Check if the database exists
   - Create the database and tables if needed
   - Insert sample data
   - Display the default admin credentials

### Method 2: Automatic Setup on App Start

The database will be automatically initialized when you start the application:

```bash
python app.py
```

If the database doesn't exist, it will be created automatically.

## Environment Configuration

Create a `.env` file in the backend directory with the following variables:

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

## Database Schema

The system creates the following tables:

### Core Tables
- `User` - System users (admin, manager, trainer, member)
- `MembershipPlan` - Available membership plans
- `Member` - Gym members
- `Trainer` - Gym trainers
- `Room` - Gym rooms and facilities

### Operational Tables
- `MembershipHistory` - Member plan history
- `FitnessClass` - Available fitness classes
- `ClassSchedule` - Class schedules
- `Attendance` - Class attendance records
- `Payments` - Payment records
- `Equipment` - Gym equipment inventory
- `Staff` - Staff members
- `EquipmentMaintenance` - Equipment maintenance records

## Sample Data

The system automatically inserts sample data:

### Membership Plans
- Basic Plan ($29.99/month)
- Standard Plan ($49.99/month)
- Premium Plan ($79.99/month)
- VIP Plan ($129.99/month)

### Rooms
- Main Gym (50 capacity)
- Cardio Room (30 capacity)
- Yoga Studio (20 capacity)
- Spin Class Room (25 capacity)
- Weight Room (40 capacity)

## Default Admin Account

After setup, you can log in with:
- Username: `admin` (or value from `ADMIN_USER` env var)
- Password: `admin` (or value from `ADMIN_PASS` env var)

## Troubleshooting

### Database Connection Issues
1. Ensure MySQL is running
2. Check database credentials in `.env` file
3. Verify the database user has proper permissions

### Permission Issues
The database user needs the following permissions:
- CREATE (for database and tables)
- INSERT, UPDATE, DELETE (for data operations)
- SELECT (for data retrieval)

### Manual Database Reset
If you need to reset the database:
1. Run the setup script: `python setup_database.py`
2. Choose 'y' when asked to reinitialize

## Features

- **Automatic Detection**: The system detects if the database exists
- **Safe Initialization**: Uses `IF NOT EXISTS` clauses to prevent errors
- **Sample Data**: Includes useful sample data for testing
- **Error Handling**: Comprehensive error handling and logging
- **Environment Based**: Uses environment variables for configuration 