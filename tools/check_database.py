import sqlite3

# Connect to the database
connection = sqlite3.connect('database/chatbot.db')
cursor = connection.cursor()

# Check the table schema
cursor.execute("PRAGMA table_info(responses)")
schema = cursor.fetchall()
print("Table Schema:")
for column in schema:
    print(column)

# Check the data in the table
cursor.execute("SELECT * FROM responses")
rows = cursor.fetchall()
print("\nTable Data:")
for row in rows:
    print(row)

connection.close()
