"""Unit tests for the validation rules on their own (no web server, no database)."""
from datetime import date

import validators as v

TODAY = date(2026, 11, 25)


def test_valid_announcement_has_no_errors():
    clean, errors = v.validate_announcement(
        {"title": "  Valid title  ", "category": "General",
         "body": "A body that is long enough.", "published_on": "2026-11-25"}, today=TODAY)
    assert errors == {}
    assert clean["title"] == "Valid title"   # spaces are trimmed


def test_body_length_boundaries():
    base = {"title": "Valid title", "category": "General", "published_on": "2026-11-25"}
    assert "body" in v.validate_announcement({**base, "body": "x" * 9}, today=TODAY)[1]
    assert "body" not in v.validate_announcement({**base, "body": "x" * 10}, today=TODAY)[1]
    assert "body" not in v.validate_announcement({**base, "body": "x" * 2000}, today=TODAY)[1]
    assert "body" in v.validate_announcement({**base, "body": "x" * 2001}, today=TODAY)[1]


def test_event_date_rules():
    base = {"title": "Valid title", "venue": "Hall", "description": "Long enough text.",
            "event_time": "10:00"}
    assert "event_date" in v.validate_event({**base, "event_date": "2026-11-24"}, today=TODAY)[1]
    assert "event_date" not in v.validate_event({**base, "event_date": "2026-11-25"}, today=TODAY)[1]
    assert "event_date" in v.validate_event({**base, "event_date": "2029-01-01"}, today=TODAY)[1]
    assert "event_date" in v.validate_event({**base, "event_date": "25/11/2026"}, today=TODAY)[1]
    assert "event_date" not in v.validate_event(
        {**base, "event_date": "2026-11-01"}, today=TODAY, allow_past=True)[1]


def test_phone_and_email_formats():
    base = {"name": "Prof. A", "designation": "Lecturer", "qualification": "M.Tech",
            "specialization": "Testing", "bio": "Teaches testing well."}
    for phone in ["98000", "5800000001", "98000000012", "98000abcde"]:
        assert "phone" in v.validate_faculty({**base, "email": "a@b.edu", "phone": phone})[1]
    for email in ["plain", "a@b", "a b@c.com", "@c.com"]:
        assert "email" in v.validate_faculty({**base, "email": email, "phone": "9800000001"})[1]
    assert v.validate_faculty({**base, "email": "A@B.Edu", "phone": "9800000001"}) [1] == {}
