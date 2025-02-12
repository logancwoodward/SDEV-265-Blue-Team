import sqlite3
from database.database_manager import DB_PATH

class ChatbotLogger:
    def __init__(self):
        """Initialize database connection."""
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def log_user_message(self, message_id, response_id, status):
        """Logs user messages and responses."""
        self.cursor.execute(
            "INSERT INTO user_logs (message_id, response_id, status) VALUES (?, ?, ?)",
            (message_id, response_id, status)
        )
        self.connection.commit()

    def log_admin_action(self, admin_id, action):
        """Logs admin actions like adding/modifying responses."""
        self.cursor.execute(
            "INSERT INTO admin_logs (admin_id, action) VALUES (?, ?)",
            (admin_id, action)
        )
        self.connection.commit()

    def close(self):
        """Closes the database connection."""
        self.connection.close()
