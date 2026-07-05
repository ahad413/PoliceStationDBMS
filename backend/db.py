import os
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ["DB_PORT"]),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
    "ssl_ca": "ca.pem"
}

def get_connection():
    return mysql.connector.connect(use_pure=True, **DB_CONFIG)


def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print("DB ERROR:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Error as e:
        print("DB ERROR:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    except Error as e:
        print("DB ERROR:", e)
        return None
    finally:
        cursor.close()
        conn.close()
