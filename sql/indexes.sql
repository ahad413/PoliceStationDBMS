USE psms;

-- STAFF SEARCH INDEXES

CREATE INDEX idx_search_staff_name
ON Staff (Name);

CREATE INDEX idx_search_staff_belt
ON Staff (BeltNo);

CREATE INDEX idx_search_staff_cnic
ON Staff (CNIC);

CREATE INDEX idx_search_staff_rank
ON Staff (RankOfficer);

CREATE INDEX idx_search_staff_status
ON Staff (Status);

-- ════════════════════════════════════════
-- FIR SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_fir_number
ON FIR (FIRNumber);

CREATE INDEX idx_search_fir_victim
ON FIR (VictimName);

CREATE INDEX idx_search_fir_cnic
ON FIR (VictimCNIC);

CREATE INDEX idx_search_fir_status
ON FIR (CaseStatus);

CREATE INDEX idx_search_fir_location
ON FIR (CrimeLocation);

-- ════════════════════════════════════════
-- DUTY SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_duty_date
ON DutyRoster (DutyDate);

CREATE INDEX idx_search_duty_division
ON DutyRoster (Division);

CREATE INDEX idx_search_duty_attendance
ON DutyRoster (AttendanceStatus);

-- ════════════════════════════════════════
-- CRIMINAL SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_criminal_name
ON WantedCriminals (Name);

CREATE INDEX idx_search_criminal_cnic
ON WantedCriminals (CNIC);

CREATE INDEX idx_search_criminal_status
ON WantedCriminals (Status);

-- ════════════════════════════════════════
-- ARREST SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_arrest_name
ON ArrestRegister (AccusedName);

CREATE INDEX idx_search_arrest_cnic
ON ArrestRegister (CNIC);

CREATE INDEX idx_search_arrest_date
ON ArrestRegister (ArrestDate);

-- ════════════════════════════════════════
-- BEAT SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_beat_name
ON Beat (BeatName);

CREATE INDEX idx_search_beat_area
ON Beat (Area);

-- ════════════════════════════════════════
-- OPERATIONS SEARCH INDEXES
-- ════════════════════════════════════════

CREATE INDEX idx_search_op_location
ON SearchOperation (Location);

CREATE INDEX idx_search_op_date
ON SearchOperation (Date);



