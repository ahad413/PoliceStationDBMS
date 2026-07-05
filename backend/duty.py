from backend.db import execute_query, fetch_all

# ═══════════════════════════════════════════════════════════
# STAFF MANAGEMENT
# ═══════════════════════════════════════════════════════════

def add_staff(belt_no, name, rank_officer, cnic, phone, address, status):
    q = """INSERT INTO staff 
           (BeltNo, Name, RankOfficer, CNIC, Phone, Address, Status)
           VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (belt_no, name, rank_officer, cnic, phone, address, status))

def get_all_staff():
    return fetch_all("SELECT * FROM staff ORDER BY BeltNo")

def update_staff_status(staff_id, status):
    return execute_query(
        "UPDATE staff SET Status = %s WHERE StaffID = %s",
        (status, staff_id)
    )

def delete_staff(staff_id):
    return execute_query(
        "DELETE FROM staff WHERE StaffID = %s",
        (staff_id,)
    )

def update_staff(staff_id, belt_no, name, rank_officer, cnic, phone, address, status):
    q = """UPDATE staff 
           SET BeltNo = %s, Name = %s, RankOfficer = %s,
               CNIC = %s, Phone = %s, Address = %s, Status = %s
           WHERE StaffID = %s"""
    return execute_query(q, (belt_no, name, rank_officer, cnic, phone, address, status, staff_id))

# ═══════════════════════════════════════════════════════════
# DUTY ROSTER
# ═══════════════════════════════════════════════════════════

def add_duty(staff_id, duty_date, division, shift, status):
    q = """INSERT INTO dutyroster 
           (StaffID, DutyDate, Division, Shift, AttendanceStatus)
           VALUES (%s,%s,%s,%s,%s)"""
    return execute_query(q, (staff_id, duty_date, division, shift, status))

def get_all_duties():
    q = """SELECT d.DutyID, s.BeltNo, s.Name, s.RankOfficer,
                  d.DutyDate, d.Division, d.Shift, d.AttendanceStatus
           FROM dutyroster d
           JOIN staff s ON d.StaffID = s.StaffID
           ORDER BY d.DutyDate DESC"""
    return fetch_all(q)

def delete_duty(duty_id):
    return execute_query(
        "DELETE FROM dutyroster WHERE DutyID = %s",
        (duty_id,)
    )

# ═══════════════════════════════════════════════════════════
# ROZNAMCHA
# ═══════════════════════════════════════════════════════════

def add_roznamcha(staff_id, date, time_out, purpose, location, time_in, remarks):
    q = """INSERT INTO roznamcha 
           (StaffID, Date, TimeOut, Purpose, Location, TimeIn, Remarks)
           VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (staff_id, date, time_out, purpose, location, time_in, remarks))

def get_all_roznamcha():
    q = """SELECT r.DiaryID, s.BeltNo, s.Name, s.RankOfficer,
                  r.Date, r.TimeOut, r.Purpose, r.Location,
                  r.TimeIn, r.Remarks
           FROM roznamcha r
           JOIN staff s ON r.StaffID = s.StaffID
           ORDER BY r.Date DESC"""
    return fetch_all(q)

def delete_roznamcha(diary_id):
    return execute_query(
        "DELETE FROM roznamcha WHERE DiaryID = %s",
        (diary_id,)
    )
