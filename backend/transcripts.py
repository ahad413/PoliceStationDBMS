import mysql.connector
from backend.db import fetch_all, fetch_one, DB_CONFIG


# ═══════════════════════════════════════════════════════════
# OFFICER TRANSCRIPT  — uses stored procedure sp_officer_profile
# ═══════════════════════════════════════════════════════════

def get_officer_profile(staff_id):
    """
    Calls sp_officer_profile which returns 5 result-sets.
    Maps them to the same dict keys the frontend already uses.
    """
    conn = mysql.connector.connect(use_pure=True, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_officer_profile', [staff_id])

        results = []
        for rs in cursor.stored_results():
            results.append(rs.fetchall())

        profile            = results[0][0] if results[0] else {}
        beat               = results[1]    if len(results) > 1 else []
        duties             = results[2]    if len(results) > 2 else []
        reported_firs      = results[3]    if len(results) > 3 else []
        investigating_firs = results[4]    if len(results) > 4 else []
        ops                = results[5]    if len(results) > 5 else []

        return {
            "profile": profile,
            "beat": beat,
            "duties": duties,
            "reported_firs": reported_firs,
            "investigating_firs": investigating_firs,
            "ops": ops,
        }
    finally:
        cursor.close()
        conn.close()


# ═══════════════════════════════════════════════════════════
# CRIMINAL DOSSIER  — uses stored procedure sp_criminal_dossier
# ═══════════════════════════════════════════════════════════

def get_criminal_profile(cnic):
    conn = mysql.connector.connect(use_pure=True, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_criminal_dossier', [cnic])

        results = []
        for rs in cursor.stored_results():
            results.append(rs.fetchall())

        wanted_info = results[0][0] if results and results[0] else None
        arrests     = results[1] if len(results) > 1 else []
        firs        = results[2] if len(results) > 2 else []

        return {
            "wanted_info": wanted_info,
            "arrests": arrests,
            "firs": firs,
        }
    finally:
        cursor.close()
        conn.close()
