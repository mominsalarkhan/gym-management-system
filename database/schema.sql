CREATE DATABASE IF NOT EXISTS gymdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gymdb;

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS MembershipPlan (
  PlanID       INT            AUTO_INCREMENT PRIMARY KEY,
  PlanName     VARCHAR(50)    NOT NULL,
  MonthlyFee   DECIMAL(8,2)   NOT NULL,
  AccessLevel  VARCHAR(20)
);

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

CREATE TABLE IF NOT EXISTS Trainer (
  TrainerID  INT AUTO_INCREMENT PRIMARY KEY,
  FirstName  VARCHAR(50) NOT NULL,
  LastName   VARCHAR(50) NOT NULL,
  Email      VARCHAR(100) NOT NULL UNIQUE,
  Specialty  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Room (
  RoomID    INT AUTO_INCREMENT PRIMARY KEY,
  RoomName  VARCHAR(50)  NOT NULL,
  Capacity  INT          NOT NULL
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

CREATE TABLE IF NOT EXISTS Equipment (
  EquipmentID    INT AUTO_INCREMENT PRIMARY KEY,
  EquipmentName  VARCHAR(50) NOT NULL,
  PurchaseDate   DATE,
  `Condition`    VARCHAR(50),
  RoomID         INT,
  FOREIGN KEY (RoomID)
    REFERENCES Room(RoomID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Staff (
  StaffID   INT AUTO_INCREMENT PRIMARY KEY,
  FirstName VARCHAR(50) NOT NULL,
  LastName  VARCHAR(50) NOT NULL,
  Email     VARCHAR(100) NOT NULL UNIQUE,
  `Role`    VARCHAR(50)
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

CREATE TABLE IF NOT EXISTS `User` (
  UserID       INT             AUTO_INCREMENT PRIMARY KEY,
  Username     VARCHAR(50)     NOT NULL UNIQUE,
  PasswordHash VARCHAR(128)    NOT NULL,
  Role         ENUM('admin','manager','trainer','member') NOT NULL
);

SET FOREIGN_KEY_CHECKS=1;