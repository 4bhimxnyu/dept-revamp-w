# Test Cases and Defect Record

**How the tests were executed:** automated with pytest (`python -m pytest -v`). Each test starts the application against a fresh temporary database, sends the same HTTP requests a browser would, and checks the response. Raw output of the run is in [test_run_output.txt](test_run_output.txt). Browser checks for layout were done in Chrome at 1280 px and 390 px; screenshots are in [screenshots/](screenshots/).

**Run recorded:** 25 November 2026, Python 3.13, Flask 3.1.3, pytest 9.1.1. **Result: 23 of 23 passed.**

Re-run the suite on the demo laptop before the jury and update the date above.

## Test cases

Type: **P** = positive (valid use works), **N** = negative (invalid use is refused), **B** = boundary or exceptional.

| ID | Type | Scenario | Steps / input | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|
| TC-01 | P | Navigation and working links | Open home; open every menu link; open one announcement and one faculty profile | Every page returns 200; home contains links to all four sections | As expected | Pass |
| TC-02 | P | **Main workflow:** admin publishes, visitor sees | Log in; create "Mid Semester Results Declared"; log out; open home and announcements | Success message; the title is visible on home and on the list | As expected | Pass |
| TC-03 | P | Admin updates an event | Create event at "Seminar Hall B"; edit venue to "Open Air Theatre"; open public events page | New venue shown, old venue gone | As expected | Pass |
| TC-04 | P | Search and filter | Search "placement"; filter category Research; search "zzzznotfound"; faculty search "machine" | Matching items only; "No announcements match" for no result | As expected | Pass |
| TC-05 | P | Contact message saved | Submit a valid message; log in as admin; open messages | Confirmation shown; message listed in admin inbox | As expected | Pass |
| TC-06 | N | **Empty fields** | Submit the announcement form with every field blank (body is spaces only) | HTTP 400; four "is required" messages; nothing saved (still 5 announcements) | As expected | Pass |
| TC-07 | N | Duplicate records | Create the same announcement title in capitals; create faculty with an email already used | Refused: "already exists" / "already uses this email" | As expected | Pass |
| TC-08 | N | Unauthorised access | Without login: open 4 admin pages, try to create an announcement, try to delete a faculty profile | Redirect to login each time; nothing created or deleted | As expected | Pass |
| TC-09 | N | Wrong login | Wrong password; unknown user; blank form | HTTP 401 and error message; admin area stays closed | As expected | Pass |
| TC-10 | N | Invalid formats | Email "not-an-email"; phone "12345"; date 2026-02-31; time 25:99; category "Hacked" | A specific message for each field; nothing saved | As expected | Pass |
| TC-11 | B | Title length limits (5 to 120) | Titles of 4, 5, 120 and 121 characters | 4 refused, 5 accepted, 120 accepted, 121 refused | As expected | Pass |
| TC-12 | B | Date limits | Event dated yesterday; event dated today; announcement dated tomorrow | Yesterday refused, today accepted, future publish date refused | As expected | Pass |
| TC-13 | B | Missing record or page | Open id 9999 for announcement, faculty, event edit; open an unknown address | Friendly "Page not found" (404), no crash | As expected | Pass |
| TC-14 | B | Form without security token | POST the contact form without the CSRF token | HTTP 400, nothing saved | As expected | Pass |
| TC-15 | B | Script typed into a field | Title `<script>alert(1)</script> Notice` | Shown as plain text (`&lt;script&gt;`), not executed | As expected | Pass |
| TC-16 | B | Empty state after deleting everything | Delete all four events; open events page | "No upcoming events are scheduled" and "There are no past events on record" | As expected | Pass |
| TC-17 | B | **Mobile layout** | Load home; inspect page and stylesheet. Manual: Chrome at 390 px, tap menu button, visit every page | Mobile viewport set, collapsible menu present; manual check: menu opens, no sideways scrolling on any page | As expected | Pass |
| TC-18 | B | Edit an old event (regression for D-03) | Edit description of an event from 14 days ago keeping its date; then try to move it to yesterday | First edit saved; second refused | As expected | Pass |
| TC-19 | B | Wildcard characters in search (regression for D-01) | Search announcements for `%`; search faculty for `_` | "No … match" message | As expected | Pass |

Four further unit tests in `tests/test_validators.py` check the validation rules directly: trimming of spaces, body length limits (9 / 10 / 2000 / 2001 characters), event date rules, and phone and email formats.

The three checks the problem statement names are covered by **TC-01 (navigation), TC-06 (empty fields) and TC-17 (mobile layout)**.

## Five test cases to show live at the jury (about 90 seconds)

1. **TC-02** positive: create an announcement as admin, show it on the home page.
2. **TC-06** negative: press Create on an empty form, show the four messages.
3. **TC-11** boundary: title "Exam" (4 characters) is refused, "Exams" (5) is accepted.
4. **TC-08** negative: log out, type `/admin` in the address bar, land on the login page.
5. **TC-17** boundary: press F12, switch to phone view, open the menu.

Then run `python -m pytest -v` in the terminal to show all 23 passing.

## Defect record

| ID | Found by | Description | Severity | Root cause | Fix | Verified by |
|---|---|---|---|---|---|---|
| D-01 | Exploratory test of search, 25 Nov 2026 | Searching for `%` or `_` returned every announcement and every faculty profile instead of "no match" | Medium | In SQL `LIKE`, `%` means "any text" and `_` means "any one character". The search word was placed inside the pattern unchanged | `like()` helper in `app.py` escapes `\`, `%` and `_`; queries use `ESCAPE '\'` | TC-19 |
| D-02 | Browser check of the empty-form screenshot, 25 Nov 2026 | On a form with errors, select boxes and text areas got a red border but text and date inputs did not | Low | The CSS rule `[aria-invalid="true"]` was weaker than the rule `input[type="text"]`, so the normal grey border won | Rule rewritten as `input[aria-invalid="true"], select[…], textarea[…]` in `style.css` | Screenshot `10_validation_errors.png`; border colour read back from the browser |
| D-03 | Design review of the event date rule | With the rule "event date cannot be in the past", an admin could not correct a typing mistake in an event that had already happened | Medium | The rule was applied on every save, not only when a date is set or changed | `validate_event(..., allow_past=True)` when the submitted date equals the stored date | TC-18 |

**Defect to explain at the jury:** D-01 is the best one. Demonstrate by saying: "We typed a percent sign into the search box and got every record back. The percent sign is a wildcard in SQL. We escaped it and added test TC-19 so it cannot come back."
