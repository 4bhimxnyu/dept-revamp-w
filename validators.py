"""Input validation rules.

Every function takes the raw form data (a dict of strings) and returns two
dicts: (clean, errors).
  clean  -> the trimmed values, safe to save.
  errors -> field name -> message shown next to that field. Empty = valid.

These are plain functions with no Flask or database code inside, so they can
be unit-tested on their own (see tests/test_validators.py).
"""
import re
from datetime import date, datetime

CATEGORIES = ["Academic", "Examination", "Placement", "Research", "General"]
DESIGNATIONS = ["Professor & Head", "Professor", "Associate Professor",
                "Assistant Professor", "Lecturer"]

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")  # 10-digit Indian mobile number


def _text(form, errors, field, label, min_len, max_len):
    """Trim a text field and check it is present and within length limits."""
    value = (form.get(field) or "").strip()
    if not value:
        errors[field] = f"{label} is required."
    elif len(value) < min_len:
        errors[field] = f"{label} must be at least {min_len} characters."
    elif len(value) > max_len:
        errors[field] = f"{label} must be at most {max_len} characters."
    return value


def _choice(form, errors, field, label, allowed):
    value = (form.get(field) or "").strip()
    if not value:
        errors[field] = f"{label} is required."
    elif value not in allowed:
        errors[field] = f"Choose a valid {label.lower()} from the list."
    return value


def _email(form, errors):
    value = (form.get("email") or "").strip().lower()
    if not value:
        errors["email"] = "Email is required."
    elif len(value) > 120 or not EMAIL_RE.match(value):
        errors["email"] = "Enter a valid email address, e.g. name@example.edu."
    return value


def _date(form, errors, field, label):
    """Parse YYYY-MM-DD. Returns a date object, or None if invalid."""
    value = (form.get(field) or "").strip()
    if not value:
        errors[field] = f"{label} is required."
        return value, None
    try:
        return value, datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        errors[field] = f"{label} must be a real date in YYYY-MM-DD format."
        return value, None


def validate_announcement(form, today=None):
    today = today or date.today()
    errors, clean = {}, {}
    clean["title"] = _text(form, errors, "title", "Title", 5, 120)
    clean["category"] = _choice(form, errors, "category", "Category", CATEGORIES)
    clean["body"] = _text(form, errors, "body", "Details", 10, 2000)
    clean["published_on"], parsed = _date(form, errors, "published_on", "Publish date")
    if parsed and parsed > today:
        errors["published_on"] = "Publish date cannot be in the future."
    return clean, errors


def validate_event(form, today=None, allow_past=False):
    """allow_past is True only when editing an old event without moving its date."""
    today = today or date.today()
    errors, clean = {}, {}
    clean["title"] = _text(form, errors, "title", "Title", 5, 120)
    clean["venue"] = _text(form, errors, "venue", "Venue", 3, 120)
    clean["description"] = _text(form, errors, "description", "Description", 10, 2000)
    clean["event_date"], parsed = _date(form, errors, "event_date", "Event date")
    if parsed and parsed < today and not allow_past:
        errors["event_date"] = "Event date cannot be in the past."
    elif parsed and parsed.year > today.year + 2:
        errors["event_date"] = "Event date is too far in the future (max 2 years ahead)."

    clean["event_time"] = (form.get("event_time") or "").strip()
    if not clean["event_time"]:
        errors["event_time"] = "Event time is required."
    else:
        try:
            datetime.strptime(clean["event_time"], "%H:%M")
        except ValueError:
            errors["event_time"] = "Event time must be in 24-hour HH:MM format."
    return clean, errors


def validate_faculty(form):
    errors, clean = {}, {}
    clean["name"] = _text(form, errors, "name", "Name", 3, 80)
    clean["designation"] = _choice(form, errors, "designation", "Designation", DESIGNATIONS)
    clean["email"] = _email(form, errors)
    clean["phone"] = (form.get("phone") or "").strip()
    if not clean["phone"]:
        errors["phone"] = "Phone is required."
    elif not PHONE_RE.match(clean["phone"]):
        errors["phone"] = "Phone must be a 10-digit mobile number starting with 6-9."
    clean["qualification"] = _text(form, errors, "qualification", "Qualification", 2, 120)
    clean["specialization"] = _text(form, errors, "specialization", "Specialization", 3, 120)
    clean["bio"] = _text(form, errors, "bio", "Profile", 10, 1500)
    return clean, errors


def validate_message(form):
    errors, clean = {}, {}
    clean["name"] = _text(form, errors, "name", "Name", 3, 80)
    clean["email"] = _email(form, errors)
    clean["subject"] = _text(form, errors, "subject", "Subject", 5, 120)
    clean["body"] = _text(form, errors, "body", "Message", 10, 1000)
    return clean, errors
