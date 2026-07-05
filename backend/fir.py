from backend.db import execute_query, fetch_all

# ═══════════════════════════════════════════════════════════════════════════
# FIR
# ═══════════════════════════════════════════════════════════════════════════

def add_fir(fir_number, datetime, victim_name, victim_cnic, victim_address,
            accused_name, accused_cnic, accused_address,
            crime_type, crime_location, distance, beat_id, reporting_officer_id,
            reporting_rank, fit_status, assigned_officer_id, case_status, fir_details):
    q = """INSERT INTO fir (FIRNumber, DateTime,
                            VictimName, VictimCNIC, VictimAddress,
                            AccusedName, AccusedCNIC, AccusedAddress,
                            CrimeType, CrimeLocation, DistanceFromStation, BeatID,
                            ReportingOfficerID, ReportingOfficerRank, FitStatus,
                            AssignedOfficerID, CaseStatus, FIRDetails)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    return execute_query(q, (
        fir_number, datetime,
        victim_name, victim_cnic, victim_address,
        accused_name, accused_cnic, accused_address,
        crime_type, crime_location, distance, beat_id,
        reporting_officer_id, reporting_rank, fit_status,
        assigned_officer_id, case_status, fir_details
    ))

def get_all_firs():
    # Uses view vw_fir_summary — same columns the frontend already expects
    q = """SELECT  f.FIRID,
                   f.FIRNumber,
                   f.DateTime,
                   f.VictimName,
                   f.VictimCNIC,
                   f.VictimAddress,
                   f.AccusedName,
                   f.AccusedCNIC,
                   f.AccusedAddress,
                   f.CrimeType,
                   f.CrimeLocation,
                   f.DistanceFromStation,
                   b.BeatName,
                   s1.Name AS ReportingOfficer,
                   s2.Name AS AssignedOfficer,
                   f.CaseStatus,
                   f.FIRDetails
            FROM   fir   f
            LEFT JOIN beat  b  ON f.BeatID            = b.BeatID
            LEFT JOIN staff s1 ON f.ReportingOfficerID = s1.StaffID
            LEFT JOIN staff s2 ON f.AssignedOfficerID  = s2.StaffID
            ORDER BY f.DateTime DESC"""
    return fetch_all(q)

def get_open_firs():
    """Return only open FIRs — uses vw_open_firs."""
    return fetch_all("SELECT * FROM vw_open_firs")

def update_fir_status(fir_id, status):
    return execute_query("UPDATE fir SET CaseStatus = %s WHERE FIRID = %s", (status, fir_id))

def delete_fir(fir_id):
    return execute_query("DELETE FROM fir WHERE FIRID = %s", (fir_id,))

# ═══════════════════════════════════════════════════════════════════════════
# ARREST REGISTER  — reads from vw_arrests_with_fir
# ═══════════════════════════════════════════════════════════════════════════

def add_arrest(fir_id, accused_name, cnic, arrest_date, arrest_location, station, remarks):
    q = """INSERT INTO arrestregister (FIRID, AccusedName, CNIC, ArrestDate,
                                       ArrestLocation, SentToPoliceStation, Remarks)
           VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (fir_id, accused_name, cnic, arrest_date,
                              arrest_location, station, remarks))

def get_all_arrests():
    return fetch_all("SELECT * FROM vw_arrests_with_fir")

def delete_arrest(arrest_id):
    return execute_query("DELETE FROM arrestregister WHERE ArrestID = %s", (arrest_id,))

# ═══════════════════════════════════════════════════════════════════════════
# CHALLAN REGISTER  — reads from vw_challan_detail
# ═══════════════════════════════════════════════════════════════════════════

def add_challan(fir_id, court_name, challan_date, fine_amount, status):
    q = """INSERT INTO challanregister (FIRID, CourtName, ChallanDate, FineAmount, Status)
           VALUES (%s,%s,%s,%s,%s)"""
    return execute_query(q, (fir_id, court_name, challan_date, fine_amount, status))

def get_all_challans():
    return fetch_all("SELECT * FROM vw_challan_detail")

def delete_challan(challan_id):
    return execute_query("DELETE FROM challanregister WHERE ChallanID = %s", (challan_id,))

# ═══════════════════════════════════════════════════════════════════════════
# WANTED CRIMINALS
# ═══════════════════════════════════════════════════════════════════════════

def add_criminal(name, cnic, crime_details, last_seen, status, fir_id=None):
    q = """INSERT INTO WantedCriminals (Name, CNIC, CrimeDetails, LastSeenLocation, Status, FIRID)
           VALUES (%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (name, cnic, crime_details, last_seen, status, fir_id))

def get_all_criminals():
    q = """SELECT w.CriminalID, w.Name, w.CNIC,
                  w.CrimeDetails, w.LastSeenLocation, w.Status,
                  f.FIRNumber
           FROM WantedCriminals w
           LEFT JOIN fir f ON w.FIRID = f.FIRID
           ORDER BY w.Status"""
    return fetch_all(q)

def update_criminal_status(criminal_id, status):
    return execute_query("UPDATE WantedCriminals SET Status = %s WHERE CriminalID = %s",
                         (status, criminal_id))

def delete_criminal(criminal_id):
    return execute_query("DELETE FROM WantedCriminals WHERE CriminalID = %s", (criminal_id,))
