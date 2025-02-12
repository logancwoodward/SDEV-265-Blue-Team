import sqlite3
import bcrypt

DB_PATH = "database/chatbot.db"

# Connect to database
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Admin credentials
admin_username = "admin"
admin_password = "admin123"  # Change this if needed

# Hash the password
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

# Insert admin user into the database
try:
    cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (admin_username, hashed_password))
    connection.commit()
    print("✅ Admin user created successfully!")
except sqlite3.IntegrityError:
    print("⚠️ Admin user already exists!")

# Close the connection
connection.close()
