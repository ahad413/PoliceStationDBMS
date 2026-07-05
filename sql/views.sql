USE psms;

-- V1
DROP VIEW IF EXISTS vw_active_staff;
CREATE VIEW vw_active_staff AS
SELECT StaffID, BeltNo, Name, RankOfficer, CNIC, Phone, Address
FROM Staff
WHERE Status = 'Active'
ORDER BY BeltNo;

-- V2
DROP VIEW IF EXISTS vw_todays_duty;
CREATE VIEW vw_todays_duty AS
SELECT d.DutyID,
       s.BeltNo,
       s.Name,
       s.RankOfficer,
       d.Division,
       d.Shift,
       d.AttendanceStatus
FROM DutyRoster d
JOIN Staff s ON d.StaffID = s.StaffID
WHERE d.DutyDate = CURDATE();

-- V3
DROP VIEW IF EXISTS vw_open_firs;
CREATE VIEW vw_open_firs AS
SELECT f.FIRID,
       f.FIRNumber,
       f.DateTime,
       f.VictimName,
       f.AccusedName,
       f.CrimeType,
       f.CrimeLocation,
       f.CaseStatus,
       s1.Name AS ReportingOfficer,
       s2.Name AS AssignedOfficer,
       b.BeatName
FROM FIR f
LEFT JOIN Beat b  ON f.BeatID = b.BeatID
LEFT JOIN Staff s1 ON f.ReportingOfficerID = s1.StaffID
LEFT JOIN Staff s2 ON f.AssignedOfficerID = s2.StaffID
WHERE f.CaseStatus = 'Open';

-- V4
DROP VIEW IF EXISTS vw_wanted_criminals;
CREATE VIEW vw_wanted_criminals AS
SELECT CriminalID, Name, CNIC, CrimeDetails, LastSeenLocation, CreatedAt
FROM WantedCriminals
WHERE Status = 'Wanted'
ORDER BY CreatedAt DESC;

-- V5
DROP VIEW IF EXISTS vw_fir_summary;
CREATE VIEW vw_fir_summary AS
SELECT f.FIRID,
       f.FIRNumber,
       DATE(f.DateTime) AS FIRDate,
       f.VictimName,
       f.AccusedName,
       f.CrimeType,
       f.CrimeLocation,
       f.CaseStatus,
       b.BeatName,
       s1.Name AS ReportingOfficer,
       s2.Name AS AssignedOfficer
FROM FIR f
LEFT JOIN Beat b ON f.BeatID = b.BeatID
LEFT JOIN Staff s1 ON f.ReportingOfficerID = s1.StaffID
LEFT JOIN Staff s2 ON f.AssignedOfficerID = s2.StaffID
ORDER BY f.DateTime DESC;

-- V6
DROP VIEW IF EXISTS vw_arrests_with_fir;
CREATE VIEW vw_arrests_with_fir AS
SELECT a.ArrestID,
       f.FIRNumber,
       f.CrimeType,
       a.AccusedName,
       a.CNIC,
       a.ArrestDate,
       a.ArrestLocation,
       a.SentToPoliceStation,
       a.Remarks
FROM ArrestRegister a
JOIN FIR f ON a.FIRID = f.FIRID
ORDER BY a.ArrestDate DESC;

-- V7
DROP VIEW IF EXISTS vw_beat_assignments;
CREATE VIEW vw_beat_assignments AS
SELECT b.BeatID,
       b.BeatName,
       b.Area,
       s.BeltNo,
       s.Name AS Officer,
       s.RankOfficer
FROM Beat b
LEFT JOIN Staff s ON b.AssignedTo = s.StaffID;

-- V8
DROP VIEW IF EXISTS vw_fund_overview;
CREATE VIEW vw_fund_overview AS
SELECT FundID,
       Source,
       AmountReceived,
       AmountUsed,
       Balance,
       Purpose,
       DateReceived
FROM GovtFund
ORDER BY DateReceived DESC;

-- V9
DROP VIEW IF EXISTS vw_fund_usage_detail;
CREATE VIEW vw_fund_usage_detail AS
SELECT u.UsageID,
       g.Source AS FundSource,
       g.AmountReceived,
       g.Balance AS RemainingBalance,
       u.AmountUsed,
       u.UsedDate,
       u.Description
FROM FundUsage u
JOIN GovtFund g ON u.FundID = g.FundID
ORDER BY u.UsedDate DESC;

-- V10
DROP VIEW IF EXISTS vw_challan_detail;
CREATE VIEW vw_challan_detail AS
SELECT c.ChallanID,
       f.FIRNumber,
       f.VictimName,
       f.AccusedName,
       c.CourtName,
       c.ChallanDate,
       c.FineAmount,
       c.Status AS PaymentStatus
FROM ChallanRegister c
JOIN FIR f ON c.FIRID = f.FIRID
ORDER BY c.ChallanDate DESC;

-- V11
DROP VIEW IF EXISTS vw_recovered_property;
CREATE VIEW vw_recovered_property AS
SELECT r.RecoveryID,
       f.FIRNumber,
       f.CrimeType,
       r.ItemName,
       r.Quantity,
       r.RecoveryDate,
       r.RecoveredFrom,
       r.Status
FROM RecoveredProperty r
JOIN FIR f ON r.FIRID = f.FIRID
ORDER BY r.RecoveryDate DESC;

-- V12
DROP VIEW IF EXISTS vw_surveillance_due;
CREATE VIEW vw_surveillance_due AS
SELECT SurveillanceID,
       PersonName,
       CNIC,
       CrimeHistory,
       ReportingInterval,
       LastReportedDate,
       NextReportingDate,
       DATEDIFF(NextReportingDate, CURDATE()) AS DaysRemaining
FROM Surveillance
WHERE NextReportingDate >= CURDATE()
ORDER BY NextReportingDate;

-- V13
DROP VIEW IF EXISTS vw_monthly_crime_stats;
CREATE VIEW vw_monthly_crime_stats AS
SELECT YEAR(DateTime) AS Year,
       MONTH(DateTime) AS Month,
       CrimeType,
       COUNT(*) AS TotalFIRs,
       SUM(CASE WHEN CaseStatus = 'Closed' THEN 1 ELSE 0 END) AS Closed,
       SUM(CASE WHEN CaseStatus = 'Open' THEN 1 ELSE 0 END) AS Open,
       SUM(CASE WHEN CaseStatus = 'Ongoing' THEN 1 ELSE 0 END) AS Ongoing
FROM FIR
GROUP BY YEAR(DateTime), MONTH(DateTime), CrimeType
ORDER BY Year DESC, Month DESC;

-- V14
DROP VIEW IF EXISTS vw_officer_workload;
CREATE VIEW vw_officer_workload AS
SELECT s.StaffID,
       s.BeltNo,
       s.Name,
       s.RankOfficer,
       COUNT(f.FIRID) AS TotalAssigned,
       SUM(CASE WHEN f.CaseStatus = 'Open' THEN 1 ELSE 0 END) AS OpenCases,
       SUM(CASE WHEN f.CaseStatus = 'Ongoing' THEN 1 ELSE 0 END) AS OngoingCases,
       SUM(CASE WHEN f.CaseStatus = 'Closed' THEN 1 ELSE 0 END) AS ClosedCases
FROM Staff s
LEFT JOIN FIR f ON s.StaffID = f.AssignedOfficerID
GROUP BY s.StaffID, s.BeltNo, s.Name, s.RankOfficer
ORDER BY TotalAssigned DESC;

-- V15
DROP VIEW IF EXISTS vw_bad_condition_assets;
CREATE VIEW vw_bad_condition_assets AS
SELECT PropertyID,
       PropertyType,
       Description,
       Quantity,
       IssueDate,
       `Condition`
FROM GovtAssets
WHERE `Condition` = 'Bad'
ORDER BY PropertyType;

-- V16
DROP VIEW IF EXISTS vw_recent_operations;
CREATE VIEW vw_recent_operations AS
SELECT o.OperationID,
       o.Date,
       o.Location,
       s.Name AS ConductedBy,
       s.RankOfficer,
       o.Reason,
       o.Result
FROM SearchOperation o
LEFT JOIN Staff s ON o.ConductedBy = s.StaffID
ORDER BY o.Date DESC;

-- V17
DROP VIEW IF EXISTS vw_pending_challans;
CREATE VIEW vw_pending_challans AS
SELECT c.ChallanID,
       f.FIRNumber,
       f.AccusedName,
       c.CourtName,
       c.ChallanDate,
       c.FineAmount
FROM ChallanRegister c
JOIN FIR f ON c.FIRID = f.FIRID
WHERE c.Status = 'Pending'
ORDER BY c.ChallanDate;

-- V18
DROP VIEW IF EXISTS vw_absent_staff;
CREATE VIEW vw_absent_staff AS
SELECT d.DutyID,
       d.DutyDate,
       s.BeltNo,
       s.Name,
       s.RankOfficer,
       d.Division,
       d.Shift
FROM DutyRoster d
JOIN Staff s ON d.StaffID = s.StaffID
WHERE d.AttendanceStatus = 'Absent'
ORDER BY d.DutyDate DESC;