import sqlite3
import bcrypt

DB_PATH = "database/chatbot.db"

class DatabaseManager:
    def __init__(self):
        """Initialize the database connection."""
        self.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates all necessary tables if they don’t exist."""
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            response TEXT NOT NULL,
            link TEXT
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            response_id INTEGER,
            status TEXT CHECK(status IN ('matched', 'unmatched')),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages(id),
            FOREIGN KEY (response_id) REFERENCES responses(id)
        );

        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        );
        ''')
        self.connection.commit()
        print("✅ Database initialized.")

    def close(self):
        """Closes the database connection."""
        self.connection.close()
from rapidfuzz import process, fuzz
import spacy


class ResponseManager:
    def __init__(self, db):
        """Manage chatbot responses."""
        self.db = db
        self.nlp = spacy.load("en_core_web_sm")  # Load Spacy model

    def get_response(self, user_message, threshold=75):
        """Fetches a chatbot response including link if available, using NLP & fuzzy matching."""
        self.db.cursor.execute("SELECT id, keyword, response, link FROM responses")
        result = self.db.cursor.fetchall()

        if not result:
            return "I don't understand that yet. Try asking something else!"

        # Build a dictionary mapping keywords (in lowercase) to their response data
        responses_dict = {row[1].lower(): (row[2], row[3], row[0]) for row in result}
        choices = list(responses_dict.keys())

        # Process user message using NLP to extract meaningful words
        doc = self.nlp(user_message.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

        best_match = None
        best_score = 0

        # Try fuzzy matching on extracted tokens
        for token in tokens:
            match, score, _ = process.extractOne(token, choices, scorer=fuzz.token_set_ratio)
            if score > best_score:
                best_match, best_score = match, score

        # Return best match if score meets threshold
        if best_match and best_score >= threshold:
            response_text, link, response_id = responses_dict[best_match]
            if link:
                return f"{response_text} <a href='{link}' target='_blank'>Learn more</a>"
            return response_text
        else:
            return "I don't understand that yet. Try asking something else!"


    def get_responses(self, page=1, per_page=10):
        """Fetch responses for admin panel with pagination."""
        offset = (page - 1) * per_page
        self.db.cursor.execute("SELECT keyword, response, link FROM responses LIMIT ? OFFSET ?", (per_page, offset))
        responses = self.db.cursor.fetchall()

        self.db.cursor.execute("SELECT COUNT(*) FROM responses")
        total_responses = self.db.cursor.fetchone()[0]

        return {
            "responses": [{"keyword": r[0], "response": r[1], "link": r[2]} for r in responses],
            "total": total_responses,
            "per_page": per_page
        }


    def add_response(self, keyword, response, link=None):
        """Add a new chatbot response."""
        try:
            self.db.cursor.execute("INSERT INTO responses (keyword, response, link) VALUES (?, ?, ?)", 
                                   (keyword, response, link))
            self.db.connection.commit()
            return {"success": "Response added successfully."}
        except sqlite3.IntegrityError:
            return {"error": "Keyword already exists."}

    def edit_response(self, old_keyword, new_keyword, new_response, new_link=None):
        """Edit an existing chatbot response, including changing the keyword."""
        self.db.cursor.execute(
        "UPDATE responses SET keyword = ?, response = ?, link = ? WHERE keyword = ?", 
        (new_keyword, new_response, new_link, old_keyword)
        )
        self.db.connection.commit()
        return {"success": "Response updated successfully."}


    def delete_response(self, keyword):
        """Delete a chatbot response."""
        self.db.cursor.execute("DELETE FROM responses WHERE keyword = ?", (keyword,))
        self.db.connection.commit()
        return {"success": "Response deleted successfully."}


class AdminManager:
    def __init__(self, db):
        """Manage admin authentication and logging actions."""
        self.db = db

    def add_admin(self, username, password):
        """Adds a new admin with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.db.cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, hashed_password))
            self.db.connection.commit()
            return {"success": "Admin added successfully."}
        except sqlite3.IntegrityError:
            return {"error": "Username already exists."}

    def verify_admin(self, username, password):
        """Verifies admin credentials."""
        self.db.cursor.execute("SELECT id, password FROM admins WHERE username = ?", (username,))
        admin_record = self.db.cursor.fetchone()

        if admin_record:
            admin_id, stored_password = admin_record
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                self.log_action(admin_id, "Admin logged in")
                return True
        return False

    def log_action(self, admin_id, action):
        """Logs admin actions (e.g., adding responses, deleting responses)."""
        self.db.cursor.execute("INSERT INTO admin_logs (admin_id, action) VALUES (?, ?)", (admin_id, action))
        self.db.connection.commit()
