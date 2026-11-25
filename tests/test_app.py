"""End-to-end test cases. IDs (TC-xx) match docs/04_test_cases.md.

Run all:  python -m pytest -v
"""
from datetime import date, timedelta

from conftest import post, token

TODAY = date.today().isoformat()
TOMORROW = (date.today() + timedelta(days=1)).isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()

GOOD_ANNOUNCEMENT = {"title": "Mid Semester Results Declared", "category": "Examination",
                     "body": "Results are available on the student portal from today.",
                     "published_on": TODAY}
GOOD_EVENT = {"title": "Sprint Review Showcase", "event_date": TOMORROW, "event_time": "14:30",
              "venue": "Seminar Hall B", "description": "Teams present their working increments."}
GOOD_FACULTY = {"name": "Prof. Test Person", "designation": "Lecturer",
                "email": "test.person@dept.example.edu", "phone": "9811111111",
                "qualification": "M.Tech", "specialization": "Software Testing",
                "bio": "Teaches software testing and quality assurance."}


# ---------- POSITIVE ----------
def test_tc01_public_pages_and_navigation_work(client):
    """TC-01: every page in the main menu opens and the home page links to them."""
    home = client.get("/")
    assert home.status_code == 200
    for path in ["/announcements", "/faculty", "/events", "/contact"]:
        assert f'href="{path}"'.encode() in home.data
        assert client.get(path).status_code == 200
    assert client.get("/announcements/1").status_code == 200
    assert client.get("/faculty/1").status_code == 200


def test_tc02_admin_creates_announcement_and_visitor_sees_it(admin, client):
    """TC-02: the main workflow. Admin publishes, visitor sees it on the site."""
    response = post(admin, "/admin/announcements/new", GOOD_ANNOUNCEMENT, follow_redirects=True)
    assert response.status_code == 200
    assert b"Announcement created" in response.data

    post(admin, "/admin/logout", {})                      # now act as a visitor
    assert b"Mid Semester Results Declared" in client.get("/").data
    assert b"Mid Semester Results Declared" in client.get("/announcements").data


def test_tc03_admin_updates_event_and_visitor_sees_change(admin):
    """TC-03: admin edits an existing event; the public page shows the new venue."""
    post(admin, "/admin/events/new", GOOD_EVENT)
    page = admin.get("/events").data
    assert b"Seminar Hall B" in page

    changed = {**GOOD_EVENT, "venue": "Open Air Theatre"}
    event_id = 5  # four seeded events + the one created above
    response = post(admin, f"/admin/events/{event_id}/edit", changed, follow_redirects=True)
    assert b"Event updated" in response.data
    page = admin.get("/events").data
    assert b"Open Air Theatre" in page and b"Seminar Hall B" not in page


def test_tc04_search_and_filter(client):
    """TC-04: search finds matching records and reports when nothing matches."""
    assert b"Placement Drive" in client.get("/announcements?q=placement").data
    assert b"Placement Drive" not in client.get("/announcements?category=Research").data
    assert b"No announcements match" in client.get("/announcements?q=zzzznotfound").data
    assert b"Deshpande" in client.get("/faculty?q=machine").data


def test_tc05_contact_message_is_saved(admin, client):
    """TC-05: a visitor's message is stored and the admin can read it."""
    response = post(client, "/contact", {"name": "Asha Rao", "email": "asha@example.com",
                                         "subject": "Admission query",
                                         "body": "Please share the admission schedule."},
                    follow_redirects=True)
    assert b"Your message was saved" in response.data
    assert b"Admission query" in admin.get("/admin/messages").data


# ---------- NEGATIVE ----------
def test_tc06_empty_fields_are_rejected(admin):
    """TC-06: submitting an empty form saves nothing and shows every error."""
    response = post(admin, "/admin/announcements/new",
                    {"title": "", "category": "", "body": "   ", "published_on": ""})
    assert response.status_code == 400
    for message in [b"Title is required.", b"Category is required.",
                    b"Details is required.", b"Publish date is required."]:
        assert message in response.data
    assert b"5 announcements found" in admin.get("/announcements").data  # still only seed data


def test_tc07_duplicate_records_are_rejected(admin):
    """TC-07: same announcement title (any letter case) and same faculty email are refused."""
    post(admin, "/admin/announcements/new", GOOD_ANNOUNCEMENT)
    again = {**GOOD_ANNOUNCEMENT, "title": GOOD_ANNOUNCEMENT["title"].upper()}
    response = post(admin, "/admin/announcements/new", again)
    assert response.status_code == 400
    assert b"already exists" in response.data

    post(admin, "/admin/faculty/new", GOOD_FACULTY)
    response = post(admin, "/admin/faculty/new", {**GOOD_FACULTY, "name": "Someone Else"})
    assert response.status_code == 400
    assert b"already uses this email" in response.data


def test_tc08_admin_area_requires_login(client):
    """TC-08: a visitor cannot open or post to the admin area."""
    for path in ["/admin", "/admin/messages", "/admin/announcements/new", "/admin/events/1/edit"]:
        response = client.get(path)
        assert response.status_code == 302 and "/admin/login" in response.headers["Location"]
    response = post(client, "/admin/announcements/new", GOOD_ANNOUNCEMENT)
    assert response.status_code == 302
    assert b"Mid Semester Results Declared" not in client.get("/announcements").data
    response = post(client, "/admin/faculty/1/delete", {})
    assert response.status_code == 302
    assert client.get("/faculty/1").status_code == 200  # not deleted


def test_tc09_wrong_login_is_rejected(client):
    """TC-09: wrong password, unknown user and blank login all fail."""
    assert post(client, "/admin/login", {"username": "admin", "password": "wrong"}).status_code == 401
    assert post(client, "/admin/login", {"username": "nobody", "password": "Admin@123"}).status_code == 401
    response = post(client, "/admin/login", {"username": "", "password": ""})
    assert b"Enter both username and password." in response.data
    assert client.get("/admin").status_code == 302


def test_tc10_invalid_formats_are_rejected(admin, client):
    """TC-10: bad email, bad phone, bad date and an unknown category are refused."""
    response = post(admin, "/admin/faculty/new",
                    {**GOOD_FACULTY, "email": "not-an-email", "phone": "12345"})
    assert b"Enter a valid email address" in response.data
    assert b"10-digit mobile number" in response.data

    response = post(admin, "/admin/events/new", {**GOOD_EVENT, "event_date": "2026-02-31",
                                                 "event_time": "25:99"})
    assert b"must be a real date" in response.data
    assert b"24-hour HH:MM" in response.data

    response = post(admin, "/admin/announcements/new", {**GOOD_ANNOUNCEMENT, "category": "Hacked"})
    assert b"Choose a valid category" in response.data

    response = post(client, "/contact", {"name": "A", "email": "a@b", "subject": "Hi", "body": "short"})
    assert response.status_code == 400


# ---------- BOUNDARY / EXCEPTIONAL ----------
def test_tc11_title_length_boundaries(admin):
    """TC-11: title of 4 chars fails, 5 passes, 120 passes, 121 fails."""
    def create(title):
        return post(admin, "/admin/announcements/new", {**GOOD_ANNOUNCEMENT, "title": title}).status_code
    assert create("A" * 4) == 400
    assert create("A" * 5) == 302
    assert create("B" * 120) == 302
    assert create("C" * 121) == 400


def test_tc12_event_date_boundaries(admin):
    """TC-12: yesterday is refused, today is accepted (the edge of the rule)."""
    past = post(admin, "/admin/events/new", {**GOOD_EVENT, "event_date": YESTERDAY})
    assert past.status_code == 400 and b"cannot be in the past" in past.data
    assert post(admin, "/admin/events/new", {**GOOD_EVENT, "event_date": TODAY}).status_code == 302
    future = post(admin, "/admin/announcements/new", {**GOOD_ANNOUNCEMENT, "published_on": TOMORROW})
    assert b"cannot be in the future" in future.data


def test_tc13_missing_records_show_404_page(admin):
    """TC-13: unknown ids and unknown addresses give a friendly 404 page, not a crash."""
    for path in ["/announcements/9999", "/faculty/9999", "/no-such-page",
                 "/admin/events/9999/edit", "/admin/unknown/new"]:
        response = admin.get(path)
        assert response.status_code == 404
        assert b"Page not found" in response.data


def test_tc14_form_without_csrf_token_is_refused(client):
    """TC-14: a form posted without the security token is rejected."""
    response = client.post("/contact", data={"name": "Asha Rao", "email": "asha@example.com",
                                             "subject": "Admission query",
                                             "body": "Please share the schedule."})
    assert response.status_code == 400


def test_tc15_html_in_input_is_escaped(admin):
    """TC-15: script tags typed into a field are shown as text, never executed."""
    data = {**GOOD_ANNOUNCEMENT, "title": "<script>alert(1)</script> Notice"}
    post(admin, "/admin/announcements/new", data)
    page = admin.get("/announcements").data
    assert b"<script>alert(1)</script>" not in page
    assert b"&lt;script&gt;" in page


def test_tc16_delete_and_empty_state(admin):
    """TC-16: after deleting every event the public page shows a clear empty message."""
    for event_id in range(1, 5):
        response = post(admin, f"/admin/events/{event_id}/delete", {})
        assert response.status_code == 302
    page = admin.get("/events").data
    assert b"No upcoming events are scheduled" in page
    assert b"There are no past events on record" in page


def test_tc17_mobile_layout_is_supported(client):
    """TC-17: the page declares a mobile viewport and ships the responsive menu."""
    page = client.get("/").data
    assert b'name="viewport"' in page and b"width=device-width" in page
    assert b'id="nav-toggle"' in page
    css = client.get("/static/style.css").data
    assert b"@media (min-width: 62rem)" in css


def test_tc18_old_event_can_be_edited_without_moving_its_date(admin):
    """TC-18: regression test for defect D-01 (see docs/04_test_cases.md)."""
    past_event_id = 4  # seeded 'Alumni Interaction Evening', 14 days ago
    old_date = (date.today() - timedelta(days=14)).isoformat()
    data = {"title": "Alumni Interaction Evening", "event_date": old_date, "event_time": "17:30",
            "venue": "Main Auditorium", "description": "Corrected description of the alumni evening."}
    assert post(admin, f"/admin/events/{past_event_id}/edit", data).status_code == 302
    moved = {**data, "event_date": YESTERDAY}
    assert post(admin, f"/admin/events/{past_event_id}/edit", moved).status_code == 400


def test_tc19_wildcard_characters_in_search_are_literal(client):
    """TC-19: regression test for defect D-01. Searching for % or _ must not match everything."""
    assert b"No announcements match" in client.get("/announcements?q=%25").data
    assert b"No faculty profiles match" in client.get("/faculty?q=_").data
