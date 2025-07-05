import os
import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection(include_db=True):
    """Get database connection with or without specifying database name"""
    config = {
        'host': os.getenv("DB_HOST", "localhost"),
        'user': os.getenv("DB_USER", "root"),
        'password': os.getenv("DB_PASS", ""),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    if include_db:
        config['database'] = os.getenv("DB_NAME", "gymdb")
    
    return mysql.connector.connect(**config)

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = get_db_connection(include_db=False)
        cursor = connection.cursor()
        
        db_name = os.getenv("DB_NAME", "gymdb")
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info(f"Database '{db_name}' created or already exists")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        logger.error(f"Error creating database: {e}")
        raise

def create_tables():
    """Create all tables if they don't exist"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        
        # SQL statements for creating tables
        tables = {
            'MembershipPlan': """
                CREATE TABLE IF NOT EXISTS MembershipPlan (
                    PlanID       INT            AUTO_INCREMENT PRIMARY KEY,
                    PlanName     VARCHAR(50)    NOT NULL,
                    MonthlyFee   DECIMAL(8,2)   NOT NULL,
                    AccessLevel  VARCHAR(20)
                )
            """,
            
            'Member': """
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
                )
            """,
            
            'MembershipHistory': """
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
                )
            """,
            
            'Trainer': """
                CREATE TABLE IF NOT EXISTS Trainer (
                    TrainerID  INT AUTO_INCREMENT PRIMARY KEY,
                    FirstName  VARCHAR(50) NOT NULL,
                    LastName   VARCHAR(50) NOT NULL,
                    Email      VARCHAR(100) NOT NULL UNIQUE,
                    Specialty  VARCHAR(100)
                )
            """,
            
            'Room': """
                CREATE TABLE IF NOT EXISTS Room (
                    RoomID    INT AUTO_INCREMENT PRIMARY KEY,
                    RoomName  VARCHAR(50)  NOT NULL,
                    Capacity  INT          NOT NULL
                )
            """,
            
            'FitnessClass': """
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
                )
            """,
            
            'ClassSchedule': """
                CREATE TABLE IF NOT EXISTS ClassSchedule (
                    ScheduleID   INT AUTO_INCREMENT PRIMARY KEY,
                    ClassID      INT NOT NULL,
                    ScheduleDate DATE NOT NULL,
                    StartTime    TIME NOT NULL,
                    EndTime      TIME NOT NULL,
                    FOREIGN KEY (ClassID)
                        REFERENCES FitnessClass(ClassID) ON DELETE CASCADE
                )
            """,
            
            'Attendance': """
                CREATE TABLE IF NOT EXISTS Attendance (
                    AttendanceID INT AUTO_INCREMENT PRIMARY KEY,
                    MemberID     INT NOT NULL,
                    ScheduleID   INT NOT NULL,
                    Status       VARCHAR(20),
                    FOREIGN KEY (MemberID)
                        REFERENCES Member(MemberID) ON DELETE CASCADE,
                    FOREIGN KEY (ScheduleID)
                        REFERENCES ClassSchedule(ScheduleID) ON DELETE CASCADE
                )
            """,
            
            'Payments': """
                CREATE TABLE IF NOT EXISTS Payments (
                    PaymentID     INT AUTO_INCREMENT PRIMARY KEY,
                    MemberID      INT NOT NULL,
                    Amount        DECIMAL(10,2) NOT NULL,
                    PaymentDate   DATE NOT NULL,
                    PaymentMethod VARCHAR(50),
                    PaymentStatus VARCHAR(20),
                    FOREIGN KEY (MemberID)
                        REFERENCES Member(MemberID) ON DELETE CASCADE
                )
            """,
            
            'Equipment': """
                CREATE TABLE IF NOT EXISTS Equipment (
                    EquipmentID    INT AUTO_INCREMENT PRIMARY KEY,
                    EquipmentName  VARCHAR(50) NOT NULL,
                    PurchaseDate   DATE,
                    `Condition`    VARCHAR(50),
                    RoomID         INT,
                    FOREIGN KEY (RoomID)
                        REFERENCES Room(RoomID) ON DELETE SET NULL
                )
            """,
            
            'Staff': """
                CREATE TABLE IF NOT EXISTS Staff (
                    StaffID   INT AUTO_INCREMENT PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName  VARCHAR(50) NOT NULL,
                    Email     VARCHAR(100) NOT NULL UNIQUE,
                    `Role`    VARCHAR(50)
                )
            """,
            
            'EquipmentMaintenance': """
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
                )
            """,
            
            'User': """
                CREATE TABLE IF NOT EXISTS `User` (
                    UserID       INT             AUTO_INCREMENT PRIMARY KEY,
                    Username     VARCHAR(50)     NOT NULL UNIQUE,
                    PasswordHash VARCHAR(128)    NOT NULL,
                    Role         ENUM('admin','manager','trainer','member') NOT NULL
                )
            """
        }
        
        # Execute table creation
        for table_name, sql in tables.items():
            cursor.execute(sql)
            logger.info(f"Table '{table_name}' created or already exists")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("All tables created successfully")
        
    except Error as e:
        logger.error(f"Error creating tables: {e}")
        raise

def insert_sample_data():
    """Insert sample data if tables are empty"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if MembershipPlan table has data
        cursor.execute("SELECT COUNT(*) FROM MembershipPlan")
        result = cursor.fetchone()
        count = result[0] if result and len(result) > 0 else 0
        
        if count == 0:
            # Insert sample membership plans
            sample_plans = [
                ("Basic Plan", 29.99, "Basic"),
                ("Standard Plan", 49.99, "Standard"),
                ("Premium Plan", 79.99, "Premium"),
                ("VIP Plan", 129.99, "VIP")
            ]
            
            cursor.executemany(
                "INSERT INTO MembershipPlan (PlanName, MonthlyFee, AccessLevel) VALUES (%s, %s, %s)",
                sample_plans
            )
            logger.info("Sample membership plans inserted")
        
        # Check if Room table has data
        cursor.execute("SELECT COUNT(*) FROM Room")
        result = cursor.fetchone()
        count = result[0] if result else 0
        
        if count == 0:
            # Insert sample rooms
            sample_rooms = [
                ("Main Gym", 50),
                ("Cardio Room", 30),
                ("Yoga Studio", 20),
                ("Spin Class Room", 25),
                ("Weight Room", 40)
            ]
            
            cursor.executemany(
                "INSERT INTO Room (RoomName, Capacity) VALUES (%s, %s)",
                sample_rooms
            )
            logger.info("Sample rooms inserted")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Error as e:
        logger.error(f"Error inserting sample data: {e}")
        raise

def initialize_database():
    """Main function to initialize the complete database"""
    try:
        logger.info("Starting database initialization...")
        
        # Step 1: Create database
        create_database()
        
        # Step 2: Create tables
        create_tables()
        
        # Step 3: Insert sample data
        insert_sample_data()
        
        logger.info("Database initialization completed successfully!")
        
    except Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def check_database_exists():
    """Check if database and tables exist"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if User table exists (key table for the system)
        cursor.execute("SHOW TABLES LIKE 'User'")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result is not None
        
    except Error:
        return False

if __name__ == "__main__":
    initialize_database() 