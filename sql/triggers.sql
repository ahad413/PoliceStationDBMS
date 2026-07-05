DELIMITER $$

-- ════════════════════════════════════════
-- STAFF TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_staff_insert
BEFORE INSERT ON Staff
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_staff_update
BEFORE UPDATE ON Staff
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- FIR TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_fir_insert
BEFORE INSERT ON FIR
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_fir_update
BEFORE UPDATE ON FIR
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- ARREST REGISTER TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_arrest_insert
BEFORE INSERT ON ArrestRegister
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_arrest_update
BEFORE UPDATE ON ArrestRegister
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- CHALLAN REGISTER TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_challan_insert
BEFORE INSERT ON ChallanRegister
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_challan_update
BEFORE UPDATE ON ChallanRegister
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- WANTED CRIMINALS TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_criminal_insert
BEFORE INSERT ON WantedCriminals
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_criminal_update
BEFORE UPDATE ON WantedCriminals
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- DUTY ROSTER TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_duty_insert
BEFORE INSERT ON DutyRoster
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_duty_update
BEFORE UPDATE ON DutyRoster
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- BEAT TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_beat_insert
BEFORE INSERT ON Beat
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_beat_update
BEFORE UPDATE ON Beat
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- BEAT BOOK TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_beatbook_insert
BEFORE INSERT ON BeatBook
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_beatbook_update
BEFORE UPDATE ON BeatBook
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- GOVT ASSETS TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_assets_insert
BEFORE INSERT ON GovtAssets
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_assets_update
BEFORE UPDATE ON GovtAssets
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- RECOVERED PROPERTY TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_recovery_insert
BEFORE INSERT ON RecoveredProperty
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_recovery_update
BEFORE UPDATE ON RecoveredProperty
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- SEARCH OPERATION TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_operation_insert
BEFORE INSERT ON SearchOperation
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_operation_update
BEFORE UPDATE ON SearchOperation
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- SURVEILLANCE TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_surveillance_insert
BEFORE INSERT ON Surveillance
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_surveillance_update
BEFORE UPDATE ON Surveillance
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- GOVT FUND TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_fund_insert
BEFORE INSERT ON GovtFund
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_fund_update
BEFORE UPDATE ON GovtFund
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- FUND USAGE TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_fundusage_insert
BEFORE INSERT ON FundUsage
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_fundusage_update
BEFORE UPDATE ON FundUsage
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- OFFICIAL CORRESPONDENCE TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_letter_insert
BEFORE INSERT ON OfficialCorrespondence
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_letter_update
BEFORE UPDATE ON OfficialCorrespondence
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- INSPECTION REGISTER TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_inspection_insert
BEFORE INSERT ON InspectionRegister
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_inspection_update
BEFORE UPDATE ON InspectionRegister
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

-- ════════════════════════════════════════
-- ROZNAMCHA TRIGGERS
-- ════════════════════════════════════════

CREATE TRIGGER trg_roznamcha_insert
BEFORE INSERT ON Roznamcha
FOR EACH ROW
BEGIN
    SET NEW.CreatedAt = NOW();
    SET NEW.UpdatedAt = NOW();
END$$

CREATE TRIGGER trg_roznamcha_update
BEFORE UPDATE ON Roznamcha
FOR EACH ROW
BEGIN
    SET NEW.UpdatedAt = NOW();
END$$

DELIMITER ;