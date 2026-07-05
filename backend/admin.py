from backend.db import execute_query, fetch_all, fetch_one

# ═══════════════════════════════════════════════════════════
# OFFICIAL CORRESPONDENCE
# ═══════════════════════════════════════════════════════════

def add_correspondence(letter_number, date, from_dept, to_dept, subject, description):
    q = """INSERT INTO officialcorrespondence
           (LetterNumber, Date, FromDepartment, ToDepartment, Subject, Description)
           VALUES (%s,%s,%s,%s,%s,%s)"""
    return execute_query(q, (letter_number, date, from_dept, to_dept, subject, description))

def get_all_correspondence():
    return fetch_all("SELECT * FROM officialcorrespondence ORDER BY Date DESC")

def delete_correspondence(letter_id):
    return execute_query(
        "DELETE FROM officialcorrespondence WHERE LetterID = %s", (letter_id,)
    )

# ═══════════════════════════════════════════════════════════
# INSPECTIONS
# ═══════════════════════════════════════════════════════════

def add_inspection(inspector_name, designation, visit_date, remarks):
    q = """INSERT INTO inspectionregister
           (InspectorName, Designation, VisitDate, Remarks)
           VALUES (%s,%s,%s,%s)"""
    return execute_query(q, (inspector_name, designation, visit_date, remarks))

def get_all_inspections():
    return fetch_all("SELECT * FROM inspectionregister ORDER BY VisitDate DESC")

def delete_inspection(insp_id):
    return execute_query(
        "DELETE FROM inspectionregister WHERE InspectionID = %s", (insp_id,)
    )

# ═══════════════════════════════════════════════════════════
# GOVERNMENT FUND  — now reads from vw_fund_overview
# ═══════════════════════════════════════════════════════════

def add_fund(source, amount_received, date_received, amount_used, purpose):
    q = """INSERT INTO govtfund
           (Source, AmountReceived, DateReceived, AmountUsed, Purpose)
           VALUES (%s,%s,%s,%s,%s)"""
    return execute_query(q, (source, amount_received, date_received, amount_used, purpose))

def get_all_funds():
    # Uses view vw_fund_overview (same columns, same order)
    return fetch_all("SELECT * FROM vw_fund_overview")

def delete_fund(fund_id):
    return execute_query("DELETE FROM govtfund WHERE FundID = %s", (fund_id,))

# ═══════════════════════════════════════════════════════════
# FUND USAGE  — now calls stored procedure sp_use_fund
# ═══════════════════════════════════════════════════════════

def use_fund(fund_id, amount_used, used_date, description):
    """
    Delegates to stored procedure sp_use_fund.
    Returns (bool, message) just like before so the frontend needs no change.
    """
    import mysql.connector
    from backend.db import DB_CONFIG          # reuse the same config dict

    conn = mysql.connector.connect(use_pure=True, **DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_use_fund', [fund_id, amount_used, used_date, description, 0, ''])
        conn.commit()

        # Fetch OUT params from the session variables MySQL sets
        cursor.execute("SELECT @_sp_use_fund_4, @_sp_use_fund_5")
        row = cursor.fetchone()
        success = bool(row[0]) if row and row[0] is not None else False
        message = row[1] if row and row[1] is not None else 'Unknown error.'
        return success, message
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_fund_usage():
    # Uses view vw_fund_usage_detail
    return fetch_all("SELECT * FROM vw_fund_usage_detail")
