DELIMITER $$
 
-- ── F1 : Get full name + rank of a staff member ────────────────────────
CREATE FUNCTION fn_staff_label(p_staff_id INT)
RETURNS VARCHAR(200)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_label VARCHAR(200);
    SELECT CONCAT(BeltNo, ' - ', Name, ' (', RankOfficer, ')')
    INTO   v_label
    FROM   Staff
    WHERE  StaffID = p_staff_id;
    RETURN IFNULL(v_label, 'Unknown');
END$$
 
-- ── F2 : Count open FIRs for a given officer ───────────────────────────
CREATE FUNCTION fn_open_cases_count(p_staff_id INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count
    FROM   FIR
    WHERE  AssignedOfficerID = p_staff_id
      AND  CaseStatus IN ('Open','Ongoing');
    RETURN IFNULL(v_count, 0);
END$$
 
-- ── F3 : Available fund balance for a given fund ───────────────────────
CREATE FUNCTION fn_fund_balance(p_fund_id INT)
RETURNS DECIMAL(12,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_balance DECIMAL(12,2);
    SELECT Balance INTO v_balance
    FROM   GovtFund
    WHERE  FundID = p_fund_id;
    RETURN IFNULL(v_balance, 0.00);
END$$
 
-- ── F4 : Check if a CNIC is in the wanted list (1/0) ──────────────────
CREATE FUNCTION fn_is_wanted(p_cnic VARCHAR(15))
RETURNS TINYINT(1)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_found TINYINT(1) DEFAULT 0;
    SELECT COUNT(*) INTO v_found
    FROM   WantedCriminals
    WHERE  CNIC   = p_cnic
      AND  Status = 'Wanted';
    RETURN v_found;
END$$
 
-- ── F5 : Total fines collected (paid challans) ─────────────────────────
CREATE FUNCTION fn_total_fines_collected()
RETURNS DECIMAL(12,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT IFNULL(SUM(FineAmount), 0.00) INTO v_total
    FROM   ChallanRegister
    WHERE  Status = 'Paid';
    RETURN v_total;
END$$
 
DELIMITER ;
