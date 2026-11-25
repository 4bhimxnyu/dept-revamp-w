# Sprint Plan, Sprint Backlog and Task Allocation

**Framework:** Scrum. Three sprints, each ending with a working, demonstrable increment.

> **Fill in before the jury:** sprint dates, team member names, retrospective notes and the "Completed" velocity column are left blank on purpose. Write what your team actually did. The evaluators will compare this document with your Jira board and GitHub commit dates, so all three must tell the same true story.

## Team and Scrum roles

| Role | Name | Main ownership |
|---|---|---|
| Product Owner (orders the backlog, accepts stories) | ________ | Backlog, acceptance criteria |
| Scrum Master (removes impediments, runs the ceremonies) | ________ | Board, DoD, risk log |
| Developer – public pages and UI | ________ | `templates/`, `static/style.css`, US-01 to US-05, US-13 |
| Developer – admin, database and validation | ________ | `app.py` admin routes, `schema.sql`, `validators.py`, US-06 to US-10 |
| Developer – testing and quality | ________ | `tests/`, defect record, US-11, US-12, US-14, US-15 |

If the team is smaller, one person holds more than one row. Each person must be able to explain the files in their row line by line.

## Ceremonies

| Ceremony | When | Output |
|---|---|---|
| Sprint Planning | First day of each sprint | Sprint goal and sprint backlog |
| Daily Scrum (15 min) | Every working day | Done yesterday / doing today / blocked by |
| Sprint Review | Last day | Demo of the working increment, feedback |
| Sprint Retrospective | After the review | One improvement for the next sprint |

## Sprint 1 – "A visitor can read everything"

Dates: ________ to ________  Capacity: 16 points

| Story | Tasks | Owner | Points | Status |
|---|---|---|---|---|
| US-01 Home and navigation | Base layout, header, footer, responsive menu, home page | ________ | 5 | Done |
| US-02 Announcements | Table, list page, detail page, empty state | ________ | 3 | Done |
| US-03 Faculty | Table, list page, detail page | ________ | 3 | Done |
| US-04 Events | Table, upcoming/past split | ________ | 3 | Done |
| US-05 Contact | Contact details, working links, footer | ________ | 2 | Done |

Increment: public site running on sample data.
Retrospective note: _write the team's real note here._

## Sprint 2 – "The office can keep it current"

Dates: ________ to ________  Capacity: 21 points

| Story | Tasks | Owner | Points | Status |
|---|---|---|---|---|
| US-06 Admin login | Hashed password, session, login-required guard, logout, CSRF token | ________ | 5 | Done |
| US-07 Manage announcements | Create, edit, delete, duplicate check | ________ | 5 | Done |
| US-08 Manage events | Create, edit, delete, date rules | ________ | 3 | Done |
| US-09 Manage faculty | Create, edit, delete, unique email | ________ | 3 | Done |
| US-10 Validation | `validators.py`, per-field messages, keep typed values | ________ | 5 | Done |

Increment: admin updates an announcement or event and the visitor sees it (the jury demo workflow).
Retrospective note: _write the team's real note here._

## Sprint 3 – "Findable, mobile-proof and tested"

Dates: ________ to ________  Capacity: 16 points

| Story | Tasks | Owner | Points | Status |
|---|---|---|---|---|
| US-11 Search and filter | Announcement search + category, faculty search | ________ | 3 | Done |
| US-12 Contact form | Form, save message, admin inbox, simulation label | ________ | 3 | Done |
| US-13 Mobile layout | Check every page at 390 px, fix overflow | ________ | 3 | Done |
| US-14 Tests and defects | 23 pytest cases, fix D-01, D-02, D-03 | ________ | 5 | Done |
| US-15 Error pages | 400, 404, 405, 413, 500 pages | ________ | 2 | Done |

Increment: release candidate for the jury.
Retrospective note: _write the team's real note here._

## Velocity

| Sprint | Planned points | Completed points (fill in) |
|---|---|---|
| 1 | 16 | ____ |
| 2 | 21 | ____ |
| 3 | 16 | ____ |
| **Average velocity** | 17.7 | ____ |

Velocity is the number of story points finished in a sprint. It is used to decide how much to commit to in the next sprint. Jira draws the velocity chart and the burndown chart automatically once the stories are in sprints with points (see [07_board_setup.md](07_board_setup.md)).

## Scope decision (Agile in practice)

The release is time-boxed to three sprints, so scope had to give. The contact **form** (US-12, 3 points) was judged more valuable to visitors than **faculty photo upload** (US-16, 5 points), so US-12 is in Sprint 3 and US-16 stays in the backlog as deferred, together with real email delivery (US-17) and multiple editor accounts (US-18). In Scrum the date is fixed and the scope moves; in a traditional plan the scope is fixed and the date moves.

If your team handled a real requirement change during the project, describe that one here instead.
