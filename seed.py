"""Sample data loaded into a new database.

ALL names, emails and phone numbers below are FICTITIOUS and exist only for
the demonstration. Dates are written relative to today so that the demo always
shows upcoming events, whenever it is run.
"""
from datetime import date, datetime, timedelta

from werkzeug.security import generate_password_hash

# Demo login. Change the password before putting this on a public host.
DEMO_ADMIN = ("admin", "Admin@123")


def _day(offset):
    return (date.today() + timedelta(days=offset)).isoformat()


def seed(db):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    db.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)",
               (DEMO_ADMIN[0], generate_password_hash(DEMO_ADMIN[1])))

    announcements = [
        ("End Semester Examination Timetable Released", "Examination",
         "The timetable for the Semester V end semester examination is now available. "
         "Students must check their seating arrangement one day before each paper and "
         "carry their identity card to the examination hall.", _day(-1)),
        ("Campus Placement Drive: Registration Open", "Placement",
         "Final year students with a CGPA of 7.0 or above may register for the upcoming "
         "placement drive. Submit an updated resume to the placement cell before the "
         "registration deadline.", _day(-3)),
        ("Call for Papers: Student Research Symposium", "Research",
         "Students are invited to submit short papers on machine learning, data analytics "
         "and software engineering. Selected papers will be presented at the symposium.",
         _day(-6)),
        ("Revised Laboratory Schedule for Semester V", "Academic",
         "The Agile Software Development laboratory has moved to Lab 204. The revised "
         "batch-wise schedule is displayed on the department notice board.", _day(-9)),
        ("Library Extended Hours During Examinations", "General",
         "The department library will remain open until 9:00 PM on all working days "
         "during the examination period.", _day(-12)),
    ]
    db.executemany(
        "INSERT INTO announcements (title, category, body, published_on, updated_at) "
        "VALUES (?, ?, ?, ?, ?)", [a + (now,) for a in announcements])

    events = [
        ("Guest Lecture: Agile at Scale", _day(5), "11:00", "Seminar Hall A",
         "An industry practitioner explains how large teams coordinate sprints, "
         "manage dependencies and keep a shared backlog."),
        ("Hands-on Workshop: Git and GitHub", _day(12), "10:00", "Computer Lab 204",
         "A practical session on branching, pull requests and resolving merge conflicts. "
         "Bring your own laptop."),
        ("Departmental Hackathon 2026", _day(21), "09:00", "Innovation Centre",
         "A 24-hour hackathon for teams of up to four students. Problem statements are "
         "announced at the opening ceremony."),
        ("Alumni Interaction Evening", _day(-14), "17:30", "Main Auditorium",
         "Alumni working in data engineering and product roles shared their career "
         "journeys with current students."),
    ]
    db.executemany(
        "INSERT INTO events (title, event_date, event_time, venue, description, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?)", [e + (now,) for e in events])

    faculty = [
        ("Dr. Meera Kulkarni", "Professor & Head", "meera.kulkarni@dept.example.edu",
         "9800000001", "Ph.D. (Computer Science)", "Software Engineering, Agile Methods",
         "Dr. Kulkarni leads the department and teaches Agile Software Development. "
         "Her research covers estimation techniques and team productivity."),
        ("Dr. Arjun Deshpande", "Professor", "arjun.deshpande@dept.example.edu",
         "9800000002", "Ph.D. (Machine Learning)", "Machine Learning, Data Analytics",
         "Dr. Deshpande works on applied machine learning and supervises the student "
         "analytics research group."),
        ("Prof. Sneha Joshi", "Associate Professor", "sneha.joshi@dept.example.edu",
         "9800000003", "M.Tech (Information Technology)", "Database Systems, Cloud Computing",
         "Prof. Joshi teaches database management systems and coordinates the "
         "department's cloud computing laboratory."),
        ("Prof. Rohan Patil", "Assistant Professor", "rohan.patil@dept.example.edu",
         "9800000004", "M.Tech (Computer Engineering)", "Web Technologies, Human-Computer Interaction",
         "Prof. Patil teaches web technologies and mentors student teams building "
         "campus applications."),
        ("Prof. Kavita Nair", "Assistant Professor", "kavita.nair@dept.example.edu",
         "9800000005", "M.E. (Computer Science)", "Computer Networks, Cyber Security",
         "Prof. Nair teaches computer networks and runs the department's security "
         "awareness club."),
    ]
    db.executemany(
        "INSERT INTO faculty (name, designation, email, phone, qualification, "
        "specialization, bio) VALUES (?, ?, ?, ?, ?, ?, ?)", faculty)
    db.commit()
