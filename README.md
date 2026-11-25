# Department Website Revamp

Agile Software Development (23CSE3012) final jury, **Problem Statement 4: Department Website Revamp – Agile vs Traditional**.

A working department website where a **visitor** reads announcements, faculty profiles, events and contact details, and an **admin (content editor)** logs in to create, update and delete that content. A change made by the admin shows on the public site immediately.

## Run it (2 commands)

Needs Python 3.10 or newer.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

| Role | How to enter | Login |
|---|---|---|
| Visitor | Just open the site | none needed |
| Admin / content editor | "Admin login" in the menu | username `admin`, password `Admin@123` |

The database file `department.db` is created automatically with sample data on first run.
To wipe it and start again from clean sample data (do this before the jury): `python app.py --reset`

## Run the tests

```bash
python -m pytest -v
```

23 automated tests (19 end-to-end, 4 unit). Results are recorded in [docs/04_test_cases.md](docs/04_test_cases.md).

## Features against the problem statement

| Required by the problem statement | Where it is |
|---|---|
| Responsive home page and navigation | `/`, menu collapses to a hamburger below 992 px |
| Announcements/news with content update capability | `/announcements` (search, category filter), admin create/edit/delete |
| Faculty profiles and details | `/faculty` (search), `/faculty/<id>` |
| Events section | `/events` (upcoming and past), admin create/edit/delete |
| Contact information and working links | `/contact`, footer links, `mailto:` and `tel:` links |
| Demo: admin updates announcement/event, visitor views it | Admin dashboard at `/admin` |
| Test navigation, empty fields, mobile layout | TC-01, TC-06, TC-17 |

## Technology

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3 | One language for the whole back end |
| Web framework | Flask 3 | Small: one route function per page |
| Database | SQLite | A single file, no server to install, built into Python |
| Pages | Jinja2 templates + plain HTML/CSS | No JavaScript framework, no internet needed at the jury |
| Tests | pytest | Runs the app in memory against a temporary database |

## Project layout

```
app.py            routes: public pages, admin pages, error pages
validators.py     input validation rules (pure functions)
seed.py           fictitious sample data + demo admin
schema.sql        database tables
templates/        HTML pages (base.html is the shared layout)
static/style.css  responsive styles
tests/            automated tests
docs/             Agile artefacts, test record, report, demo script
```

## What is simulated (stated plainly)

- **All data is fictitious**: department address, faculty names, emails, phone numbers, announcements and events are sample data.
- **Contact form "delivery" is simulated**: the message is really saved to the database and the admin can really read it, but no email is sent.
- There is no payment, GPS, sensor or third-party API in this project.

## Documentation

1. [Product backlog and user stories](docs/01_product_backlog_user_stories.md)
2. [Sprint plan, sprint backlog and task allocation](docs/02_sprint_plan.md)
3. [Definition of Done, risks and impediments](docs/03_definition_of_done_and_risks.md)
4. [Test cases and defect record](docs/04_test_cases.md)
5. [Project report: architecture, database, Agile vs Traditional](docs/05_project_report.md)
6. [Jury demo script and viva preparation](docs/06_jury_demo_script.md)
7. [Jira import file](docs/jira_import.csv) and [how to set up the board](docs/07_board_setup.md)
