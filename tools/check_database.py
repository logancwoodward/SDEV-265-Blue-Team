import sqlite3
import os

# Path to the database file
DB_PATH = "database/chatbot.db"

def check_database():
    """Checks the database schema and sample data from all tables."""

    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database file not found at {DB_PATH}")
        return

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("❌ No tables found in the database.")
        return

    print("\n📌 Database Structure Overview\n" + "="*40)

    for table in tables:
        table_name = table[0]
        print(f"\n🔹 Checking table: {table_name}")

        # Fetch table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()

        if not schema:
            print("  ⚠️ No schema found for this table.")
        else:
            print("  📂 Schema:")
            for column in schema:
                print(f"    - {column[1]} ({column[2]})")

        # Fetch sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")  # Increased sample size
        rows = cursor.fetchall()
        if rows:
            print("  📊 Sample Data:")
            for row in rows:
                print("    ", row)
        else:
            print("  ⚠️ No data in this table.")

    connection.close()
    print("\n✅ Database check complete.")

# Run the check
if __name__ == "__main__":
    check_database()
