import sqlite3

# Path to the database file
DB_PATH = "database/chatbot.db"

# Create the database and table
def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        response TEXT NOT NULL,
        link TEXT
    )
    ''')
    connection.commit()
    connection.close()
    print("Database and table initialized.")

# Insert sample data into the table
def insert_sample_data():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    sample_data = [
        ("Ivy Tech", "Ivy Tech is a great community college!", "https://www.ivytech.edu"),
        ("courses", "Explore the Ivy Tech course catalog.", "https://www.ivytech.edu/courses"),
        ("admissions", "For admissions, visit the Ivy Tech Admissions page.", "https://www.ivytech.edu/admissions"),
        ("financial aid", "Learn more about Ivy Tech financial aid.", "https://www.ivytech.edu/financial-aid")
    ]

    cursor.executemany("INSERT INTO responses (keyword, response, link) VALUES (?, ?, ?)", sample_data)
    connection.commit()
    connection.close()
    print("Sample data inserted.")

# Run these functions only when this script is executed directly
if __name__ == "__main__":
    create_database()
    insert_sample_data() # Commented out to avoid inserting duplicate data; enable only if resetting the database
