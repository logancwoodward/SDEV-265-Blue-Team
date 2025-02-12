import sqlite3

# Path to the database file
DB_PATH = "database/chatbot.db"

def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create Responses Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        response TEXT NOT NULL,
        link TEXT
    )
    ''')

    # Create Messages Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create User Logs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        response_id INTEGER,
        status TEXT CHECK(status IN ('matched', 'unmatched')),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (message_id) REFERENCES messages(id),
        FOREIGN KEY (response_id) REFERENCES responses(id)
    )
    ''')

    # Create Admins Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Create Admin Logs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (admin_id) REFERENCES admins(id)
    )
    ''')

    connection.commit()
    connection.close()
    print("Database initialized successfully.")

# Run this file to create the database
if __name__ == "__main__":
    create_database()
