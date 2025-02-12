import sqlite3

# Path to your SQLite database
DB_PATH = "database/chatbot.db"

# 50 chatbot responses (with some optional links)
sample_responses = [
    ("hello", "Hello! How can I assist you?"),
    ("admissions", "For admissions, visit the Ivy Tech Admissions page.", "https://www.ivytech.edu/admissions"),
    ("courses", "Explore the Ivy Tech course catalog.", "https://www.ivytech.edu/courses"),
    ("financial aid", "Learn more about Ivy Tech financial aid.", "https://www.ivytech.edu/financial-aid"),
    ("degrees", "Ivy Tech offers diverse degree programs.", "https://catalog.ivytech.edu/"),
    ("apply", "Ready to apply? Start your journey at Ivy Tech.", "https://www.ivytech.edu/admissions"),
    ("arts", "Ivy Tech offers Associate of Arts degrees."),
    ("accounting", "Crunching numbers and balancing books? Check out our Accounting programs.", "https://catalog.ivytech.edu/"),
    ("fine arts", "Express your creativity and turn your passion into a career."),
    ("visual arts", "Bring your designs to life with Ivy Tech’s Visual Arts programs."),
    ("class format", "At Ivy Tech, classes are available online and in-person."),
    ("programs", "Here are all of our wonderful Ivy Tech programs.", "https://www.ivytech.edu/programs/"),
    ("tutoring", "Need help? Ivy Tech offers tutoring services.", "https://www.ivytech.edu/tutoring/"),
    ("housing", "Ivy Tech does not offer housing, but we provide resources to find options."),
    ("internships", "Explore internships and career opportunities at Ivy Tech."),
    ("scholarships", "Apply for scholarships to support your education."),
    ("career services", "Career Services can help you with job placement and resume building."),
    ("library", "Find books, resources, and study materials in the Ivy Tech Library."),
    ("parking", "Learn about parking permits and regulations."),
    ("sports", "Check out Ivy Tech's sports and recreation programs."),
    ("student life", "Get involved in student organizations and activities!"),
    ("graduation", "Learn about graduation requirements and ceremonies."),
    ("events", "Check out upcoming events and important dates."),
    ("registration", "Register for classes through MyIvy."),
    ("technical support", "Need IT help? Contact Ivy Tech Tech Support."),
    ("email", "Access your Ivy Tech email via MyIvy."),
    ("canvas", "Log in to Canvas for your online classes."),
    ("student handbook", "Check the student handbook for policies and resources."),
    ("academic calendar", "View the academic calendar for important dates."),
    ("transcripts", "Request your official Ivy Tech transcripts."),
    ("financial services", "Manage your tuition payments and financial accounts."),
    ("advising", "Meet with an academic advisor for guidance."),
    ("bookstore", "Purchase textbooks and school supplies from the bookstore."),
    ("clubs", "Join student clubs and organizations at Ivy Tech."),
    ("volunteer", "Find volunteer opportunities in your community."),
    ("study abroad", "Explore Ivy Tech’s study abroad programs."),
    ("fitness", "Stay active with Ivy Tech's fitness programs."),
    ("veterans", "Support services for veterans and military students."),
    ("diversity", "Learn about Ivy Tech's commitment to diversity and inclusion."),
    ("faculty", "Find faculty directories and contact information."),
    ("staff", "Connect with Ivy Tech staff for support."),
    ("ID card", "Get your Ivy Tech student ID card."),
    ("health services", "Access student health services and resources."),
    ("mental health", "Find mental health support and counseling."),
    ("student discounts", "Get student discounts at various retailers."),
    ("career fairs", "Attend career fairs to network with employers."),
    ("research", "Find research opportunities and resources."),
    ("technology", "Explore Ivy Tech's technology courses."),
    ("study tips", "Find study tips to improve your learning experience."),
    ("business degrees", "Discover Ivy Tech's business degree programs."),
    ("computer science", "Learn about Ivy Tech’s Computer Science programs."),
]

# Insert missing responses
def insert_responses():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for row in sample_responses:
        keyword = row[0]
        response = row[1]
        link = row[2] if len(row) == 3 else None  # Handle optional link

        # Check if the keyword already exists
        cursor.execute("SELECT COUNT(*) FROM responses WHERE keyword = ?", (keyword,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute("INSERT INTO responses (keyword, response, link) VALUES (?, ?, ?)", (keyword, response, link))
            print(f"✅ Added: {keyword}")
        else:
            print(f"⚠️ Skipped (already exists): {keyword}")

    connection.commit()
    connection.close()
    print("✅ Data insertion complete.")

if __name__ == "__main__":
    insert_responses()
