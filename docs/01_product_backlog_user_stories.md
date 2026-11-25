# Product Backlog and User Stories

**Product goal:** replace the outdated department website with one that visitors can use on a phone and that the department office can keep current without a developer.

**Users**
- **Visitor**: student, parent or applicant who reads information. No account.
- **Admin (content editor)**: department office staff who publish and correct content.

**Prioritisation:** MoSCoW (Must / Should / Could / Won't this release). **Estimation:** story points on the Fibonacci scale (1, 2, 3, 5, 8). The points below are a proposed starting estimate; re-estimate them together with Planning Poker and change any your team disagrees with. A story point measures relative effort, not hours: a 5 is roughly as much work as a 2 and a 3 together.

## Prioritised backlog

| Rank | ID | Story (short) | Priority | Points | Sprint | Status |
|---|---|---|---|---|---|---|
| 1 | US-01 | Responsive home page and navigation | Must | 5 | 1 | Done |
| 2 | US-02 | View announcements and details | Must | 3 | 1 | Done |
| 3 | US-03 | View faculty profiles and details | Must | 3 | 1 | Done |
| 4 | US-04 | View upcoming and past events | Must | 3 | 1 | Done |
| 5 | US-05 | Contact information and working links | Must | 2 | 1 | Done |
| 6 | US-06 | Admin login and logout | Must | 5 | 2 | Done |
| 7 | US-07 | Admin manages announcements | Must | 5 | 2 | Done |
| 8 | US-08 | Admin manages events | Must | 3 | 2 | Done |
| 9 | US-09 | Admin manages faculty profiles | Should | 3 | 2 | Done |
| 10 | US-10 | Input validation and clear error messages | Must | 5 | 2 | Done |
| 11 | US-11 | Search and filter | Should | 3 | 3 | Done |
| 12 | US-12 | Contact form and admin inbox | Should | 3 | 3 | Done |
| 13 | US-13 | Mobile layout check and fixes | Must | 3 | 3 | Done |
| 14 | US-14 | Automated tests and defect fixes | Must | 5 | 3 | Done |
| 15 | US-15 | Friendly error pages | Could | 2 | 3 | Done |
| 16 | US-16 | Faculty photo upload | Could | 5 | – | Deferred |
| 17 | US-17 | Real email notification for contact form | Won't | 5 | – | Deferred |
| 18 | US-18 | Several editor accounts with separate permissions | Won't | 8 | – | Deferred |

Planned and implemented: **53 points** across 3 sprints (16 + 21 + 16). "Done" means the story is implemented in the code and covered by a passing test.

## User stories with acceptance criteria

Format: *As a (role), I want (goal), so that (benefit).* Acceptance criteria use Given / When / Then.

### US-01 Responsive home page and navigation
As a visitor, I want a home page with a clear menu, so that I can reach any section in one click from a phone or a laptop.
- Given any page, when I look at the header, then I see links to Home, Announcements, Faculty, Events and Contact.
- Given a screen narrower than 992 px, when the page loads, then the menu is collapsed behind a menu button and opens when I tap it.
- Given the home page, then it shows the 3 latest announcements and the next 3 upcoming events.
- Given a 390 px wide phone screen, then no page scrolls sideways.

### US-02 View announcements and details
As a visitor, I want to read announcements, so that I do not miss notices.
- Given the announcements page, then announcements are listed newest first with category and date.
- When I open an announcement, then I see its full text and when it was last updated.
- Given there are no announcements, then I see "No announcements have been published yet" instead of a blank page.

### US-03 View faculty profiles and details
As a visitor, I want to see faculty profiles, so that I know whom to contact for a subject.
- Given the faculty page, then each faculty member shows name, designation and specialization.
- When I open a profile, then I see qualification, email, phone and a short profile.
- Email and phone are clickable links.

### US-04 View upcoming and past events
As a visitor, I want to see events, so that I can plan to attend.
- Upcoming events are listed soonest first with date, time and venue.
- Events whose date has passed appear under "Past events".
- If there are no upcoming events, a clear message is shown.

### US-05 Contact information and working links
As a visitor, I want the department's contact details, so that I can reach the office.
- The contact page shows address, email, phone and office hours.
- Every link in the menu and footer opens a working page (no broken links).

### US-06 Admin login and logout
As an admin, I want to log in, so that only authorised staff can change content.
- Given correct username and password, when I log in, then I reach the dashboard.
- Given a wrong username or password, then I see "Incorrect username or password" and stay logged out.
- Given I am not logged in, when I open any `/admin` page, then I am sent to the login page.
- Passwords are stored hashed, never as plain text.

### US-07 Admin manages announcements
As an admin, I want to create, edit and delete announcements, so that notices stay current.
- When I create a valid announcement, then it appears on the public site immediately.
- When I edit an announcement, then visitors see the new text.
- When I delete an announcement, I am asked to confirm, and then it disappears from the public site.
- A second announcement with the same title is refused.

### US-08 Admin manages events
As an admin, I want to create, edit and delete events, so that the calendar is accurate.
- A new event must have a date of today or later.
- The same title on the same date is refused as a duplicate.
- An old event can still be corrected without changing its date.

### US-09 Admin manages faculty profiles
As an admin, I want to add and update faculty profiles, so that the directory is accurate.
- Email must be valid and unique; phone must be a 10-digit mobile number.
- Designation must be chosen from the fixed list.

### US-10 Input validation and clear error messages
As an admin, I want to be told exactly what is wrong with a form, so that I can fix it quickly.
- Empty required fields are refused with a message next to each field.
- Text that is too short or too long is refused with the allowed limits stated.
- When a form has errors, nothing is saved and what I typed is kept.

### US-11 Search and filter
As a visitor, I want to search, so that I find a notice or a teacher quickly.
- Searching announcements matches title and text; filtering by category works with or without a search word.
- Searching faculty matches name, designation and specialization.
- When nothing matches, a clear "no match" message is shown.

### US-12 Contact form and admin inbox
As a visitor, I want to send a message, so that I can ask the office a question.
- A valid message is saved and I see a confirmation.
- The admin can read all messages, newest first.
- The page states that no email is sent (simulated delivery).

### US-13 Mobile layout check and fixes
As a visitor on a phone, I want every page to fit my screen.
- All pages checked at 390 px width with no sideways scrolling.
- Tables in the admin area scroll inside their own box.

### US-14 Automated tests and defect fixes
As the team, we want automated tests, so that a change does not silently break a feature.
- At least 5 test cases covering positive, negative and boundary scenarios (23 delivered).
- Every defect found has a regression test.

### US-15 Friendly error pages
As a visitor, I want a helpful page when something is missing, so that I am not shown a technical error.
- An unknown address or record shows a "Page not found" page with a link home.
