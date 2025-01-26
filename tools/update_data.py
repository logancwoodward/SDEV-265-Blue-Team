import sqlite3

# Path to your database file
DB_PATH = "database/chatbot.db"

# Function to update a specific response
def update_response(response_id, keyword, response, link):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE responses
        SET keyword = ?, response = ?, link = ?
        WHERE id = ?
    """, (keyword, response, link, response_id))

    connection.commit()
    connection.close()
    print(f"Response with ID {response_id} updated successfully.")

# Example usage (modify these values as needed)
if __name__ == "__main__":
    update_response(
        response_id=11,  # The ID of the response to update
        keyword="fine",
        response="Express your creativity and turn your passion into a career with Ivy Tech's Fine Arts program. Ready to create something amazing?",
        link="https://catalog.ivytech.edu/preview_program.php?catoid=7&poid=5833&returnto=766"
    )
