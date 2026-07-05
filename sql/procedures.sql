DELIMITER $$
 
-- ── P1 : Get complete officer profile in one call ──────────────────────
CREATE PROCEDURE sp_officer_profile(IN p_staff_id INT)
BEGIN
    -- 1. Basic profile
    SELECT StaffID, BeltNo, Name, RankOfficer, CNIC, Phone, Address, Status
    FROM   Staff
    WHERE  StaffID = p_staff_id;
 
    -- 2. Assigned beat
    SELECT BeatName, Area
    FROM   Beat
    WHERE  AssignedTo = p_staff_id;
 
    -- 3. Last 10 duty records
    SELECT DutyDate, Division, Shift, AttendanceStatus
    FROM   DutyRoster
    WHERE  StaffID  = p_staff_id
    ORDER BY DutyDate DESC
    LIMIT 10;
 
    -- 4. Assigned (investigating) FIRs
    SELECT FIRNumber, DATE(DateTime) AS FIRDate, CrimeType, CaseStatus
    FROM   FIR
    WHERE  AssignedOfficerID = p_staff_id
    ORDER BY DateTime DESC;
 
    -- 5. Operations conducted
    SELECT Date, Location, Result
    FROM   SearchOperation
    WHERE  ConductedBy = p_staff_id
    ORDER BY Date DESC;
END$$
 
-- ── P2 : File an FIR and optionally link accused to wanted list ─────────
CREATE PROCEDURE sp_file_fir(
    IN p_fir_number        VARCHAR(30),
    IN p_datetime          DATETIME,
    IN p_victim_name       VARCHAR(100),
    IN p_victim_cnic       VARCHAR(15),
    IN p_victim_address    VARCHAR(255),
    IN p_accused_name      VARCHAR(100),
    IN p_accused_cnic      VARCHAR(15),
    IN p_accused_address   VARCHAR(255),
    IN p_crime_type        VARCHAR(100),
    IN p_crime_location    VARCHAR(200),
    IN p_distance          DECIMAL(6,2),
    IN p_beat_id           INT,
    IN p_reporting_id      INT,
    IN p_reporting_rank    VARCHAR(50),
    IN p_fit_status        VARCHAR(50),
    IN p_assigned_id       INT,
    IN p_case_status       ENUM('Open','Closed','Ongoing'),
    IN p_fir_details       TEXT,
    IN p_add_to_wanted     TINYINT(1)   -- 1 = add accused to wanted list
)
BEGIN
    DECLARE v_fir_id INT;
 
    INSERT INTO FIR (
        FIRNumber, DateTime,
        VictimName, VictimCNIC, VictimAddress,
        AccusedName, AccusedCNIC, AccusedAddress,
        CrimeType, CrimeLocation, DistanceFromStation,
        BeatID, ReportingOfficerID, ReportingOfficerRank,
        FitStatus, AssignedOfficerID, CaseStatus, FIRDetails
    ) VALUES (
        p_fir_number, p_datetime,
        p_victim_name, p_victim_cnic, p_victim_address,
        p_accused_name, p_accused_cnic, p_accused_address,
        p_crime_type, p_crime_location, p_distance,
        p_beat_id, p_reporting_id, p_reporting_rank,
        p_fit_status, p_assigned_id, p_case_status, p_fir_details
    );
 
    SET v_fir_id = LAST_INSERT_ID();
 
    IF p_add_to_wanted = 1 AND p_accused_cnic IS NOT NULL THEN
        -- Only insert if not already in wanted list
        IF NOT EXISTS (
            SELECT 1 FROM WantedCriminals
            WHERE CNIC = p_accused_cnic AND Status = 'Wanted'
        ) THEN
            INSERT INTO WantedCriminals (Name, CNIC, CrimeDetails, Status, FIRID)
            VALUES (p_accused_name, p_accused_cnic, p_crime_type, 'Wanted', v_fir_id);
        END IF;
    END IF;
 
    SELECT v_fir_id AS NewFIRID;
END$$
 
-- ── P3 : Use fund with balance validation ──────────────────────────────
CREATE PROCEDURE sp_use_fund(
    IN  p_fund_id     INT,
    IN  p_amount      DECIMAL(12,2),
    IN  p_used_date   DATE,
    IN  p_description VARCHAR(255),
    OUT p_success     TINYINT(1),
    OUT p_message     VARCHAR(255)
)
BEGIN
    DECLARE v_balance DECIMAL(12,2);
 
    SELECT Balance INTO v_balance
    FROM   GovtFund
    WHERE  FundID = p_fund_id;
 
    IF v_balance IS NULL THEN
        SET p_success = 0;
        SET p_message = 'Fund not found.';
    ELSEIF p_amount <= 0 THEN
        SET p_success = 0;
        SET p_message = 'Amount must be greater than zero.';
    ELSEIF p_amount > v_balance THEN
        SET p_success = 0;
        SET p_message = 'Insufficient balance.';
    ELSE
        INSERT INTO FundUsage (FundID, AmountUsed, UsedDate, Description)
        VALUES (p_fund_id, p_amount, p_used_date, p_description);
 
        UPDATE GovtFund
        SET    AmountUsed = AmountUsed + p_amount
        WHERE  FundID = p_fund_id;
 
        SET p_success = 1;
        SET p_message = 'Fund used successfully.';
    END IF;
END$$
 
-- ── P4 : Mark wanted criminal as arrested & auto-close if needed ────────
CREATE PROCEDURE sp_mark_arrested(
    IN p_criminal_id      INT,
    IN p_fir_id           INT,
    IN p_accused_name     VARCHAR(100),
    IN p_cnic             VARCHAR(15),
    IN p_arrest_date      DATE,
    IN p_arrest_location  VARCHAR(200),
    IN p_station          VARCHAR(150),
    IN p_remarks          TEXT
)
BEGIN
    -- Update wanted status
    UPDATE WantedCriminals
    SET    Status = 'Arrested'
    WHERE  CriminalID = p_criminal_id;
 
    -- Log the arrest
    INSERT INTO ArrestRegister (
        FIRID, AccusedName, CNIC, ArrestDate,
        ArrestLocation, SentToPoliceStation, Remarks
    ) VALUES (
        p_fir_id, p_accused_name, p_cnic, p_arrest_date,
        p_arrest_location, p_station, p_remarks
    );
 
    SELECT ROW_COUNT() AS RowsAffected;
END$$
 
-- ── P5 : Dashboard summary counts (used by home page) ─────────────────
CREATE PROCEDURE sp_dashboard_summary()
BEGIN
    SELECT
        (SELECT COUNT(*) FROM Staff WHERE Status = 'Active')                       AS ActiveStaff,
        (SELECT COUNT(*) FROM FIR   WHERE CaseStatus IN ('Open','Ongoing'))        AS OpenFIRs,
        (SELECT COUNT(*) FROM WantedCriminals WHERE Status = 'Wanted')             AS WantedCriminals,
        (SELECT IFNULL(SUM(Balance),0) FROM GovtFund)                              AS TotalFundBalance,
        (SELECT COUNT(*) FROM DutyRoster WHERE DutyDate = CURDATE()
            AND AttendanceStatus = 'Present')                                      AS PresentToday,
        (SELECT COUNT(*) FROM ArrestRegister
            WHERE ArrestDate BETWEEN DATE_SUB(CURDATE(),INTERVAL 30 DAY)
                                 AND CURDATE())                                    AS ArrestsThisMonth;
END$$
 
-- ── P6 : Get full criminal dossier by CNIC ─────────────────────────────
CREATE PROCEDURE sp_criminal_dossier(IN p_cnic VARCHAR(15))
BEGIN
    -- Wanted info
    SELECT * FROM WantedCriminals WHERE CNIC = p_cnic;
 
    -- Arrest history
    SELECT a.ArrestDate, a.ArrestLocation, f.FIRNumber, f.CaseStatus
    FROM   ArrestRegister a
    JOIN   FIR f ON a.FIRID = f.FIRID
    WHERE  a.CNIC = p_cnic;
 
    -- Linked FIRs
    SELECT f.FIRNumber, DATE(f.DateTime) AS FIRDate,
           f.VictimName, f.CrimeType, f.CaseStatus
    FROM   FIR f
    JOIN   ArrestRegister a ON f.FIRID = a.FIRID
    WHERE  a.CNIC = p_cnic;
END$$
 
-- ── P7 : Monthly attendance report for a staff member ─────────────────
CREATE PROCEDURE sp_monthly_attendance(
    IN p_staff_id INT,
    IN p_year     INT,
    IN p_month    INT
)
BEGIN
    SELECT  d.DutyDate,
            d.Division,
            d.Shift,
            d.AttendanceStatus
    FROM    DutyRoster d
    WHERE   d.StaffID    = p_staff_id
      AND   YEAR(d.DutyDate)  = p_year
      AND   MONTH(d.DutyDate) = p_month
    ORDER BY d.DutyDate;
 
    -- Summary counts
    SELECT
        COUNT(*)                                                          AS TotalDays,
        SUM(CASE WHEN AttendanceStatus='Present' THEN 1 ELSE 0 END)      AS Present,
        SUM(CASE WHEN AttendanceStatus='Absent'  THEN 1 ELSE 0 END)      AS Absent
    FROM DutyRoster
    WHERE StaffID    = p_staff_id
      AND YEAR(DutyDate)  = p_year
      AND MONTH(DutyDate) = p_month;
END$$
 
DELIMITER 