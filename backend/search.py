from backend.db import fetch_all

# ═══════════════════════════════════════════════════════════
# STAFF SEARCH
# ═══════════════════════════════════════════════════════════

def search_staff(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT StaffID, BeltNo, Name, RankOfficer,
                  CNIC, Phone, Address, Status
           FROM staff
           WHERE Name       LIKE %s
              OR BeltNo     LIKE %s
              OR CNIC       LIKE %s
              OR RankOfficer LIKE %s
              OR Status     LIKE %s
           ORDER BY BeltNo"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))

# ═══════════════════════════════════════════════════════════
# DUTY SEARCH
# ═══════════════════════════════════════════════════════════

def search_duty(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT d.DutyID, s.BeltNo, s.Name, s.RankOfficer,
                  d.DutyDate, d.Division, d.Shift, d.AttendanceStatus
           FROM dutyroster d
           JOIN staff s ON d.StaffID = s.StaffID
           WHERE s.Name            LIKE %s
              OR s.BeltNo          LIKE %s
              OR d.Division        LIKE %s
              OR d.AttendanceStatus LIKE %s
              OR CAST(d.DutyDate AS CHAR) LIKE %s
           ORDER BY d.DutyDate DESC"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))

# ═══════════════════════════════════════════════════════════
# FIR SEARCH
# ═══════════════════════════════════════════════════════════

def search_fir(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT f.FIRID, f.FIRNumber, f.DateTime,
                  f.VictimName, f.VictimCNIC,
                  f.AccusedName, f.AccusedCNIC,
                  f.CrimeType, f.CrimeLocation, 
                  f.CaseStatus, f.FIRDetails,
                  b.BeatName,
                  s1.Name AS ReportingOfficer,
                  s2.Name AS AssignedOfficer
           FROM fir f
           LEFT JOIN beat  b  ON f.BeatID            = b.BeatID
           LEFT JOIN staff s1 ON f.ReportingOfficerID = s1.StaffID
           LEFT JOIN staff s2 ON f.AssignedOfficerID  = s2.StaffID
           WHERE f.FIRNumber     LIKE %s
              OR f.VictimName    LIKE %s
              OR f.VictimCNIC    LIKE %s
              OR f.AccusedName   LIKE %s
              OR f.AccusedCNIC   LIKE %s
              OR f.CrimeType     LIKE %s
              OR f.CrimeLocation LIKE %s
              OR f.CaseStatus    LIKE %s
              OR s1.Name         LIKE %s
              OR s2.Name         LIKE %s
           ORDER BY f.DateTime DESC"""
    return fetch_all(q, (
        keyword, keyword, keyword,
        keyword, keyword, keyword,
        keyword, keyword, keyword, keyword
    ))

# ═══════════════════════════════════════════════════════════
# WANTED CRIMINALS SEARCH
# ═══════════════════════════════════════════════════════════

def search_criminals(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT CriminalID, Name, CNIC,
                  CrimeDetails, LastSeenLocation, Status
           FROM WantedCriminals
           WHERE Name            LIKE %s
              OR CNIC            LIKE %s
              OR CrimeDetails    LIKE %s
              OR LastSeenLocation LIKE %s
              OR Status          LIKE %s
           ORDER BY Status"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))

# ═══════════════════════════════════════════════════════════
# ARREST SEARCH
# ═══════════════════════════════════════════════════════════

def search_arrests(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT a.ArrestID, f.FIRNumber,
                  a.AccusedName, a.CNIC,
                  a.ArrestDate, a.ArrestLocation,
                  a.SentToPoliceStation, a.Remarks
           FROM arrestregister a
           JOIN fir f ON a.FIRID = f.FIRID
           WHERE a.AccusedName         LIKE %s
              OR a.CNIC                LIKE %s
              OR f.FIRNumber           LIKE %s
              OR a.ArrestLocation      LIKE %s
              OR a.SentToPoliceStation LIKE %s
           ORDER BY a.ArrestDate DESC"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))

# ═══════════════════════════════════════════════════════════
# BEAT RECORDS SEARCH
# ═══════════════════════════════════════════════════════════

def search_beats(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT bb.BeatRecordID, b.BeatName, b.Area,
                  s.BeltNo, s.Name AS Officer,
                  bb.Date, bb.ActivityDetails, bb.Remarks
           FROM beatbook bb
           JOIN beat  b ON bb.BeatID  = b.BeatID
           JOIN staff s ON bb.StaffID = s.StaffID
           WHERE b.BeatName        LIKE %s
              OR b.Area            LIKE %s
              OR s.Name            LIKE %s
              OR s.BeltNo          LIKE %s
              OR bb.ActivityDetails LIKE %s
           ORDER BY bb.Date DESC"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))

# ═══════════════════════════════════════════════════════════
# SEARCH OPERATIONS SEARCH
# ═══════════════════════════════════════════════════════════

def search_operations(keyword):
    keyword = f"%{keyword}%"
    q = """SELECT o.OperationID, o.Date, o.Location,
                  s.Name AS ConductedBy,
                  o.Reason, o.Result
           FROM searchoperation o
           LEFT JOIN staff s ON o.ConductedBy = s.StaffID
           WHERE o.Location LIKE %s
              OR o.Reason   LIKE %s
              OR o.Result   LIKE %s
              OR s.Name     LIKE %s
              OR CAST(o.Date AS CHAR) LIKE %s
           ORDER BY o.Date DESC"""
    return fetch_all(q, (keyword, keyword, keyword, keyword, keyword))
