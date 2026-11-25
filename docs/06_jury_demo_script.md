# Jury Demo Script and Viva Preparation

Follows the "Suggested Final Jury Demonstration Sequence" in the guidelines. Total about 11 minutes plus viva.

## Before you enter the room

- [ ] `python app.py --reset` then `python app.py` and leave it running
- [ ] Browser tab 1: http://127.0.0.1:5000 (visitor). Tab 2 (a private/incognito window): http://127.0.0.1:5000/admin/login
- [ ] Terminal ready in the project folder for `python -m pytest -v`
- [ ] Jira board and GitHub repository open in two more tabs (these need internet; keep screenshots as a fallback)
- [ ] Login noted: `admin` / `Admin@123`

## 1. Problem and users (1 minute)

"The department website is hard to use on a phone and goes out of date because every change needs a developer. Our users are visitors, who only read, and the department office, who must update content themselves. We built a responsive site with a login-protected admin area. It is Python Flask with a SQLite database."

## 2. Live prototype (5–7 minutes)

| Step | Do | Say |
|---|---|---|
| 1 | Visitor tab: home page, click through Announcements, Faculty (open one profile), Events, Contact | "All five required sections. Every link works." |
| 2 | Search announcements for "placement", then filter by Examination | "Search and category filter." |
| 3 | Admin tab: type `/admin` without logging in | "The admin area is protected: we are sent to login." |
| 4 | Log in | "Passwords are stored hashed." |
| 5 | Add announcement: title "Jury Demo: Lab Closed on Friday", category General, today's date, any details. Create | "Green confirmation." |
| 6 | **Visitor tab: refresh home** | "The visitor sees it immediately. This is the core workflow." |
| 7 | Admin: edit the event "Guest Lecture: Agile at Scale", change venue to "Main Auditorium". Visitor tab: Events | "Update works for events too." |
| 8 | Visitor: Contact, send a message. Admin: Contact messages | "The message is saved to the database. No email is sent; that part is simulated and labelled on the page." |
| 9 | F12 → phone view (or narrow the window), open the menu | "Responsive layout with a collapsible menu." |

## 3. Testing (1–2 minutes)

1. Empty form → Create: four messages, nothing saved. (negative, TC-06)
2. Title "Exam" → refused, "at least 5 characters". Title "Exams" → accepted. (boundary, TC-11)
3. Same title again → "already exists". (negative, TC-07)
4. Open `/announcements/9999` → friendly 404. (exceptional, TC-13)
5. Terminal: `python -m pytest -v` → 23 passed.

Defect to explain: "Searching for a percent sign returned every record, because percent is a wildcard in SQL LIKE. We escaped it and added regression test TC-19." Show `docs/04_test_cases.md`.

## 4. Agile evidence (2 minutes)

- Jira: backlog ordered by priority with story points; three sprints; board columns; burndown and velocity reports.
- One user story with acceptance criteria (US-07 is a good one).
- Definition of Done (`docs/03`), risk register.
- GitHub: commit history, tests folder, the Actions tab showing tests passing.
- Agile vs Traditional table in the report (`docs/05`, section 7): this is the theme of our problem statement.

## 5. Viva: questions each member should be able to answer

**Architecture**
- *What happens when I click Create?* Browser sends a POST → CSRF token checked → login checked → `validators.py` checks each field → duplicate check → SQL INSERT → redirect with a success message.
- *Why Flask and SQLite?* Smallest tools that meet the requirement: one Python file for the server, one file for the database, nothing to install on the demo laptop, works offline.
- *What is a route?* A Python function that Flask calls for a given address. `@app.route("/events")` means "run this function when someone opens /events".
- *What is a template?* An HTML file with placeholders like `{{ row.title }}` that Flask fills with data from the database.

**Security**
- *How are passwords stored?* As a salted hash made by `generate_password_hash`. A hash is a one-way scramble; at login we hash what was typed and compare.
- *What is CSRF and how do you stop it?* Cross-Site Request Forgery: another website tricks a logged-in admin's browser into submitting a form to our site. We put a random token in the session and in every form; a POST without the matching token gets a 400.
- *How do you prevent SQL injection?* Every query uses `?` placeholders, so user text is sent as data and never becomes part of the SQL command.
- *What if someone types a script tag?* Jinja2 escapes output automatically, so `<script>` is displayed as text. Test TC-15.

**Validation and testing**
- *Why validate on the server when the browser can do it?* Browser checks can be bypassed by sending a request directly. The server is the only place we control.
- *What is a boundary test?* Testing the edges of a rule: for "5 to 120 characters" we test 4, 5, 120 and 121.
- *How do the tests avoid touching real data?* Each test creates the app with a temporary database file that is thrown away afterwards.

**Agile**
- *What is a story point?* A relative measure of effort. Not hours.
- *What is velocity?* Story points completed per sprint; used to plan the next sprint.
- *What is your Definition of Done?* Acceptance criteria pass, server-side validation, a passing automated test, works on mobile, committed, peer reviewed, accepted by the Product Owner.
- *What did you defer and why?* Photo upload, real email and multiple editor roles: lower value than the core update workflow in a fixed three-sprint timebox.
- *Agile vs Traditional in one line?* Traditional fixes scope and lets the date move; Agile fixes the date and lets scope move, delivering working software every sprint.

**Honest answers to have ready**
- *Is the contact form sending email?* No. It saves to the database. It is labelled as simulated.
- *Is this deployed?* It runs locally, which the guidelines allow.
- *Is the data real?* No, all names and contact details are fictitious sample data.
