from backend.db import execute_query, fetch_all

# ═══════════════════════════════════════════════════════════════════════════
# SEARCH OPERATIONS (Register 8)
# ═══════════════════════════════════════════════════════════════════════════

def add_operation(date, location, conducted_by, reason, result):
    q = """INSERT INTO searchoperation (Date, Location, ConductedBy, Reason, Result)
           VALUES (%s,%s,%s,%s,%s)"""
    return execute_query(q, (date, location, conducted_by if conducted_by else None,
                              reason, result))

def get_all_operations():
    q = """SELECT o.OperationID, o.Date, o.Location,
                  s.Name AS ConductedBy, o.Reason, o.Result
           FROM searchoperation o
           LEFT JOIN staff s ON o.ConductedBy = s.StaffID
           ORDER BY o.Date DESC"""
    return fetch_all(q)

def delete_operation(op_id):
    return execute_query("DELETE FROM searchoperation WHERE OperationID = %s", (op_id,))

# ═══════════════════════════════════════════════════════════════════════════
# SURVEILLANCE (Register 10)
# ═══════════════════════════════════════════════════════════════════════════

def add_surveillance(person_name, cnic, crime_history, reporting_interval,
                     last_reported, next_reporting):
    q = """INSERT INTO surveillance (PersonName, CNIC, CrimeHistory, ReportingInterval,
                                     LastReportedDate, NextReportingDate)
           VALUES (%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (person_name, cnic, crime_history, reporting_interval,
                              last_reported, next_reporting))

def get_all_surveillance():
    return fetch_all("SELECT * FROM surveillance ORDER BY NextReportingDate")

def delete_surveillance(surv_id):
    return execute_query("DELETE FROM surveillance WHERE SurveillanceID = %s", (surv_id,))
