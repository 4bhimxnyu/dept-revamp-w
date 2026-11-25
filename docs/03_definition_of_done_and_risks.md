# Definition of Done, Risks and Impediments

## Definition of Done (DoD)

A user story is "Done" only when **all** of these are true:

1. Every acceptance criterion of the story passes when checked by hand in the browser.
2. All user input for the feature is validated on the server, with a clear message for each rule.
3. At least one automated test covers the story, and the whole suite passes (`python -m pytest`).
4. The page works at 390 px (phone) and 1280 px (laptop) with no sideways scrolling.
5. No broken links and no raw error page can be reached from the feature.
6. Code is committed to GitHub with a message that says what changed and why.
7. Another team member has read the change (peer review).
8. Any simulated behaviour is labelled on the screen and in the README.
9. The Product Owner has accepted the story at the sprint review.

## Definition of Ready (before a story enters a sprint)

- Written in "As a…, I want…, so that…" form with acceptance criteria.
- Estimated in story points by the whole team.
- Small enough to finish in one sprint, with no unresolved dependency.

## Risk register

Score = probability (1–3) × impact (1–3).

| ID | Risk | P | I | Score | Mitigation | Status |
|---|---|---|---|---|---|---|
| R-01 | No internet or blocked network in the jury room | 2 | 3 | 6 | App runs fully offline: local Flask server, SQLite file, no CDN fonts or scripts | Mitigated |
| R-02 | Demo data is messy after practice runs | 3 | 2 | 6 | `python app.py --reset` restores clean sample data in one command | Mitigated |
| R-03 | A late change breaks a working feature | 2 | 3 | 6 | 23 automated tests run before every commit; CI workflow in `.github/workflows` | Mitigated |
| R-04 | Unauthorised person changes content | 2 | 3 | 6 | Login required on every admin route, hashed password, CSRF token on every form | Mitigated |
| R-05 | Malicious input (script tags, SQL) | 2 | 3 | 6 | Templates escape all output; all SQL uses `?` placeholders; tests TC-15 and TC-19 | Mitigated |
| R-06 | A team member cannot explain their part in the viva | 2 | 3 | 6 | Code owners listed in the sprint plan; walkthrough rehearsal; viva questions in doc 06 | Open – rehearse |
| R-07 | Python or Flask missing on the demo laptop | 1 | 3 | 3 | `requirements.txt`; install and run once on the demo laptop the day before | Open – check |
| R-08 | Scope creep (photo upload, email) | 2 | 2 | 4 | Deferred to backlog as US-16, US-17 by the Product Owner | Closed |

## Technical challenges and how they were resolved

| ID | Challenge | Resolution |
|---|---|---|
| C-01 | The "event date cannot be in the past" rule would stop the admin from correcting details of an old event | Rule relaxed only when the date itself is unchanged (defect D-03, test TC-18) |
| C-02 | Tests sharing one database would affect each other | Each test gets its own temporary database (`tests/conftest.py`) |
| C-03 | Forms carry a security (CSRF) token, so tests cannot post a bare form | A test helper reads the token from the session before posting, like a browser |
| C-04 | Searching for `%` or `_` matched every record | Wildcard characters are escaped before the SQL `LIKE` (defect D-01, test TC-19) |

## Impediment log (fill in)

An impediment is anything that blocked the team, not the code: a member unavailable, no access to Jira, a merge conflict that cost a day.

| ID | Impediment | Sprint | Resolution |
|---|---|---|---|
| I-01 | ________ | __ | ________ |
