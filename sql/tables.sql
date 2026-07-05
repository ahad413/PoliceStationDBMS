CREATE DATABASE IF NOT EXISTS psms;
USE psms;

CREATE TABLE Staff (
    StaffID     INT AUTO_INCREMENT PRIMARY KEY,
    Name        VARCHAR(100) NOT NULL,
    Rankofficer       VARCHAR(50)  NOT NULL,
    CNIC        VARCHAR(15)  NOT NULL UNIQUE,
    Phone       VARCHAR(15),
    Address     VARCHAR(255),
    Status      ENUM('Active', 'Suspended') DEFAULT 'Active'
);

CREATE TABLE Beat (
    BeatID      INT AUTO_INCREMENT PRIMARY KEY,
    BeatName    VARCHAR(100) NOT NULL,
    Area        VARCHAR(150),
    AssignedTo  INT,
    FOREIGN KEY (AssignedTo) REFERENCES Staff(StaffID) ON DELETE SET NULL
);

-- Module 1: Duty & Attendance

CREATE TABLE DutyRoster (
    DutyID           INT AUTO_INCREMENT PRIMARY KEY,
    StaffID          INT NOT NULL,
    DutyDate         DATE NOT NULL,
    Division         ENUM('Investigation', 'Operation') NOT NULL,
    Shift            VARCHAR(50) NOT NULL,
    AttendanceStatus ENUM('Present', 'Absent') DEFAULT 'Present',
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

CREATE TABLE Roznamcha (
    DiaryID  INT AUTO_INCREMENT PRIMARY KEY,
    StaffID  INT NOT NULL,
    Date     DATE NOT NULL,
    TimeOut  TIME NOT NULL,
    Purpose  VARCHAR(255) NOT NULL,
    Location VARCHAR(200) NOT NULL,
    TimeIn   TIME,
    Remarks  TEXT,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Module 2: FIR & Crime Management

CREATE TABLE FIR (
    FIRID                INT AUTO_INCREMENT PRIMARY KEY,
    FIRNumber            VARCHAR(30) NOT NULL UNIQUE,
    DateTime             DATETIME NOT NULL,
    VictimName           VARCHAR(100) NOT NULL,
    VictimCNIC           VARCHAR(15),
    VictimAddress        VARCHAR(255),
    CrimeLocation        VARCHAR(200) NOT NULL,
    DistanceFromStation  DECIMAL(6,2),
    BeatID               INT,
    ReportingOfficerID   INT,
    ReportingOfficerRank VARCHAR(50),
    FitStatus            VARCHAR(50),
    AssignedOfficerID    INT,
    CaseStatus           ENUM('Open', 'Closed', 'Ongoing') DEFAULT 'Open',
    FOREIGN KEY (BeatID)             REFERENCES Beat(BeatID)   ON DELETE SET NULL,
    FOREIGN KEY (ReportingOfficerID) REFERENCES Staff(StaffID) ON DELETE SET NULL,
    FOREIGN KEY (AssignedOfficerID)  REFERENCES Staff(StaffID) ON DELETE SET NULL
);

CREATE TABLE ArrestRegister (
    ArrestID            INT AUTO_INCREMENT PRIMARY KEY,
    FIRID               INT NOT NULL,
    AccusedName         VARCHAR(100) NOT NULL,
    CNIC                VARCHAR(15),
    ArrestDate          DATE NOT NULL,
    ArrestLocation      VARCHAR(200),
    SentToPoliceStation VARCHAR(150),
    Remarks             TEXT,
    FOREIGN KEY (FIRID) REFERENCES FIR(FIRID) ON DELETE CASCADE
);

CREATE TABLE ChallanRegister (
    ChallanID   INT AUTO_INCREMENT PRIMARY KEY,
    FIRID       INT NOT NULL,
    CourtName   VARCHAR(150) NOT NULL,
    ChallanDate DATE NOT NULL,
    FineAmount  DECIMAL(10,2),
    Status      ENUM('Paid', 'Pending') DEFAULT 'Pending',
    FOREIGN KEY (FIRID) REFERENCES FIR(FIRID) ON DELETE CASCADE
);

CREATE TABLE WantedCriminals (
    CriminalID       INT AUTO_INCREMENT PRIMARY KEY,
    Name             VARCHAR(100) NOT NULL,
    CNIC             VARCHAR(15),
    CrimeDetails     TEXT,
    LastSeenLocation VARCHAR(200),
    Status           ENUM('Wanted', 'Arrested') DEFAULT 'Wanted'
);

-- Module 3: Property Management

CREATE TABLE GovtAssets (
    PropertyID   INT AUTO_INCREMENT PRIMARY KEY,
    PropertyType ENUM('Weapon', 'Vehicle', 'Furniture', 'Facility') NOT NULL,
    Description  VARCHAR(200),
    Quantity     INT NOT NULL DEFAULT 1,
    IssueDate    DATE,
   `Condition` ENUM('Good', 'Bad') DEFAULT 'Good'
);

CREATE TABLE RecoveredProperty (
    RecoveryID    INT AUTO_INCREMENT PRIMARY KEY,
    FIRID         INT NOT NULL,
    ItemName      VARCHAR(150) NOT NULL,
    Quantity      INT DEFAULT 1,
    RecoveryDate  DATE NOT NULL,
    RecoveredFrom VARCHAR(150),
    Status        ENUM('Returned', 'Kept') DEFAULT 'Kept',
    FOREIGN KEY (FIRID) REFERENCES FIR(FIRID) ON DELETE CASCADE
);

-- Module 4: Beat & Patrol

CREATE TABLE BeatBook (
    BeatRecordID    INT AUTO_INCREMENT PRIMARY KEY,
    BeatID          INT NOT NULL,
    StaffID         INT NOT NULL,
    Date            DATE NOT NULL,
    ActivityDetails TEXT NOT NULL,
    Remarks         TEXT,
    FOREIGN KEY (BeatID)  REFERENCES Beat(BeatID)   ON DELETE CASCADE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Module 5: Operations & Surveillance

CREATE TABLE SearchOperation (
    OperationID INT AUTO_INCREMENT PRIMARY KEY,
    Date        DATE NOT NULL,
    Location    VARCHAR(200) NOT NULL,
    ConductedBy INT,
    Reason      TEXT,
    Result      TEXT,
    FOREIGN KEY (ConductedBy) REFERENCES Staff(StaffID) ON DELETE SET NULL
);

CREATE TABLE Surveillance (
    SurveillanceID    INT AUTO_INCREMENT PRIMARY KEY,
    PersonName        VARCHAR(100) NOT NULL,
    CNIC              VARCHAR(15),
    CrimeHistory      TEXT,
    ReportingInterval VARCHAR(50),
    LastReportedDate  DATE,
    NextReportingDate DATE
);

-- Module 6: Administration & Finance

CREATE TABLE OfficialCorrespondence (
    LetterID       INT AUTO_INCREMENT PRIMARY KEY,
    LetterNumber   VARCHAR(50) NOT NULL UNIQUE,
    Date           DATE NOT NULL,
    FromDepartment VARCHAR(150),
    ToDepartment   VARCHAR(150),
    Subject        VARCHAR(255),
    Description    TEXT
);

CREATE TABLE InspectionRegister (
    InspectionID  INT AUTO_INCREMENT PRIMARY KEY,
    InspectorName VARCHAR(100) NOT NULL,
    Designation   VARCHAR(100),
    VisitDate     DATE NOT NULL,
    Remarks       TEXT
);

CREATE TABLE GovtFund (
    FundID INT AUTO_INCREMENT PRIMARY KEY,
    Source VARCHAR(200) NOT NULL,
    AmountReceived DECIMAL(12,2) NOT NULL CHECK (AmountReceived >= 0),
    DateReceived DATE NOT NULL,
    AmountUsed DECIMAL(12,2) DEFAULT 0.00 CHECK (AmountUsed >= 0),
    Purpose VARCHAR(255),
    Balance DECIMAL(12,2)
    GENERATED ALWAYS AS (AmountReceived - AmountUsed) STORED
);
-- use psms;
CREATE TABLE FundUsage (
    UsageID INT AUTO_INCREMENT PRIMARY KEY,
    FundID INT NOT NULL,
    AmountUsed DECIMAL(12,2) NOT NULL,
    UsedDate DATE NOT NULL,
    Description VARCHAR(255),
    FOREIGN KEY (FundID) REFERENCES GovtFund(FundID) ON DELETE CASCADE
);



-- Check beat records
SELECT COUNT(*) FROM BeatBook;

-- Check operations records  
SELECT COUNT(*) FROM SearchOperation;

ALTER TABLE FIR 
ADD COLUMN AccusedName VARCHAR(100) AFTER VictimAddress,
ADD COLUMN AccusedCNIC VARCHAR(15) AFTER AccusedName,
ADD COLUMN AccusedAddress VARCHAR(255) AFTER AccusedCNIC;


ALTER TABLE FIR 
ADD COLUMN FIRDetails TEXT;

ALTER TABLE FIR 
ADD COLUMN CrimeType VARCHAR(100);

ALTER TABLE WantedCriminals ADD FIRID INT NULL;
ALTER TABLE WantedCriminals ADD CONSTRAINT FK_WantedCriminals_FIR 
    FOREIGN KEY (FIRID) REFERENCES FIR(FIRID);


SHOW TABLES from psms;
