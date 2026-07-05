from db import get_connection, fetch_all

try:
    conn = get_connection()
    print("✅ Connection Successful!")

    # Test query
    result = fetch_all("SHOW TABLES;")
    print(f"Tables: {result}")

except Exception as e:
    print(f"❌ Error: {e}")