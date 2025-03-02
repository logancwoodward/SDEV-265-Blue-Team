import sqlite3

# Path to your SQLite database
DB_PATH = "database/chatbot.db"

# 50 chatbot responses (with some optional links)
sample_responses = [
    ("Ivytech", "Ivy Tech is a great community college!", "https://www.ivytech.edu/"),
    ("admissions", "For admissions, visit the Ivy Tech Admissions page.", "https://www.ivytech.edu/admissions"),
    ("courses", "Explore the Ivy Tech course catalog.", "https://www.ivytech.edu/courses"),
    ("financial aid", "Learn more about Ivy Tech financial aid.", "https://www.ivytech.edu/financial-aid"),
    ("degrees", "Ivy Tech offers diverse degree programs to help you advance your career. Ready to start your journey?", "https://catalog.ivytech.edu/content.php?catoid=7&navoid=766"),
    ("apply", "Ready to apply? Start your journey at Ivy Tech today and take the first step toward your future!", "https://www.ivytech.edu/admissions/apply-now/"),
    ("arts", "Ivy Tech offers Associate of Arts programs in Liberal Arts, Fine Arts, Visual Communications, and Culinary Arts."),
    ("accounting", "Crunching numbers and balancing books—at Ivy Tech, our Accounting program prepares you for a career in finance. Ready to dive in?", "https://catalog.ivytech.edu/preview_program.php?catoid=7&poid=5836&returnto=766"),
    ("fine", "Express your creativity and turn your passion into a career with Ivy Tech's Fine Arts program. Ready to create something amazing?", "https://catalog.ivytech.edu/preview_program.php?catoid=7&poid=5833&returnto=766"),
    ("visual", "Bring your designs to life with Ivy Tech's Visual Communications program—where creativity meets technology. Want to learn more?", "https://catalog.ivytech.edu/preview_program.php?catoid=7&poid=5834&returnto=766"),
    ("password", "Your username and password to the online verification center are the same as your MyIvy account. If you are locked out, contact the IT Help Desk.", "https://ivytech.edusupportcenter.com/shp/ivytech/article?articleId=1510211"),
    ("advanced automationrobotics", "Ready to work with robots? The Advanced Automation & Robotics program teaches you how to design, maintain, and operate high-tech manufacturing systems.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/advanced-automation-robotics-technology/"),
    ("advising", "Need help with academic advising? Visit our advising page for support and schedule an appointment.", "https://www.ivytech.edu/student-services/advising/"),
    ("agriculture", "Passionate about farming and sustainability? The Agriculture program covers modern farming techniques, agribusiness, and environmental science.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/advanced-automation-robotics-technology/"),
    ("aid", "You can apply for financial aid by filling out the FAFSA form.", "https://www.ivytech.edu/tuition-aid/financial-aid/"),
    ("automotive", "Love working on cars? The Automotive Technology program trains you in diagnostics, repair, and vehicle systems.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/automotive-technology/"),
    ("aviation", "Aviation covers several exciting career paths! Are you interested in:\n- Aviation Maintenance\n- Aviation Management\n- Flight Training"),
    ("maintenance", "Keep planes flying! The Aviation Maintenance Technology program teaches aircraft repair and inspection.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/aviation-maintenance-technology/"),
    ("management", "Take your career to the skies! The Aviation Management program focuses on airport operations, airline management, and logistics.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/aviation-management/"),
    ("flight", "Dream of becoming a pilot? The Aviation Flight program prepares you for FAA certification with hands-on flight training.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/aviation-technology-flight/"),
    ("biology", "Explore the science of life! The Biology program prepares you for careers in healthcare, research, and environmental science.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-arts-sciences-education/biology/"),
    ("biotechnology", "Curious about DNA, lab research, and medical breakthroughs? The Biotechnology program trains you in genetics, microbiology, and pharmaceutical development.", "https://www.ivytech.edu/programs/all-academic-programs/school-of-advanced-manufacturing-engineering-applied-science/biotechnology/"),
    ("library", "Find books, resources, and study materials in the Ivy Tech Library.", "https://www.ivytech.edu/student-services/libraries/"),
    ("graduation", "Graduation applications and requirements can be found here.", "https://www.ivytech.edu/locations/hamilton-county/graduation-info/"),
    ("helpdesk", "Need technical assistance? Call 1-888-IVY-LINE (888-489-5469), option 4.", "https://myivy.ivytech.edu"),
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
