"""Department Website (Problem Statement 4: Department Website Revamp).

Run:   python app.py            -> http://127.0.0.1:5000
Reset: python app.py --reset    -> deletes the database and loads sample data

How a request flows:
  browser -> Flask route (this file) -> validators.py -> SQLite (department.db)
          -> Jinja2 template (templates/) -> HTML back to the browser
"""
import os
import secrets
import sqlite3
import sys
from datetime import date, datetime
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash

import seed as seed_data
import validators as v

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel sets VERCEL=1. Its project folder is read-only and only /tmp can be
# written, so the hosted demo keeps its database there. /tmp is temporary: the
# hosted site goes back to the sample data whenever Vercel starts a new instance.
ON_VERCEL = bool(os.environ.get("VERCEL"))
DEFAULT_DB = os.environ.get("DATABASE_PATH") or (
    "/tmp/department.db" if ON_VERCEL else os.path.join(BASE_DIR, "department.db"))

# Fixed details of the department shown on every page (sample values).
DEPARTMENT = {
    "name": "Department of Computer Science & Engineering",
    "short": "CSE Department",
    "tagline": "B.Tech CSE (AI & Analytics)",
    "address": "Academic Block C, Second Floor, University Campus (sample address)",
    "email": "office@dept.example.edu",
    "phone": "020-5550-0100",
    "hours": "Monday to Friday, 9:00 AM to 5:00 PM",
}

# One entry per content type the admin can manage. The admin routes below are
# written once and use this table to know which database table, which columns
# and which validation function belong to each type.
CONTENT = {
    "announcements": {
        "label": "Announcement", "table": "announcements", "order": "published_on DESC, id DESC",
        "columns": ["title", "category", "body", "published_on"],
        "name_column": "title",
        "fields": [
            {"name": "title", "label": "Title", "type": "text", "max": 120, "help": "5 to 120 characters."},
            {"name": "category", "label": "Category", "type": "select", "options": v.CATEGORIES},
            {"name": "published_on", "label": "Publish date", "type": "date", "help": "Today or earlier."},
            {"name": "body", "label": "Details", "type": "textarea", "max": 2000, "help": "10 to 2000 characters."},
        ],
    },
    "events": {
        "label": "Event", "table": "events", "order": "event_date DESC, id DESC",
        "columns": ["title", "event_date", "event_time", "venue", "description"],
        "name_column": "title",
        "fields": [
            {"name": "title", "label": "Title", "type": "text", "max": 120, "help": "5 to 120 characters."},
            {"name": "event_date", "label": "Event date", "type": "date", "help": "Today or later."},
            {"name": "event_time", "label": "Event time", "type": "time"},
            {"name": "venue", "label": "Venue", "type": "text", "max": 120},
            {"name": "description", "label": "Description", "type": "textarea", "max": 2000, "help": "10 to 2000 characters."},
        ],
    },
    "faculty": {
        "label": "Faculty profile", "table": "faculty", "order": "id ASC",
        "columns": ["name", "designation", "email", "phone", "qualification", "specialization", "bio"],
        "name_column": "name",
        "fields": [
            {"name": "name", "label": "Name", "type": "text", "max": 80},
            {"name": "designation", "label": "Designation", "type": "select", "options": v.DESIGNATIONS},
            {"name": "email", "label": "Email", "type": "email", "max": 120, "help": "Must be unique."},
            {"name": "phone", "label": "Phone", "type": "text", "max": 10, "help": "10-digit mobile number."},
            {"name": "qualification", "label": "Qualification", "type": "text", "max": 120},
            {"name": "specialization", "label": "Specialization", "type": "text", "max": 120},
            {"name": "bio", "label": "Profile", "type": "textarea", "max": 1500, "help": "10 to 1500 characters."},
        ],
    },
}


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DATABASE"] = db_path or DEFAULT_DB
    # The secret key signs the login cookie. Set SECRET_KEY in the environment on a real host.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    if ON_VERCEL:  # the hosted site is always HTTPS, so never send the login cookie over HTTP
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # reject request bodies above 64 KB

    # ---------- database helpers ----------
    def get_db():
        """One connection per request, stored on Flask's `g` object."""
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row  # rows behave like dicts: row["title"]
        return g.db

    @app.teardown_appcontext
    def close_db(_error):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        """Create the tables and load sample data if the database is empty."""
        with app.app_context():
            db = get_db()
            with open(os.path.join(BASE_DIR, "schema.sql"), encoding="utf-8") as f:
                db.executescript(f.read())
            if db.execute("SELECT COUNT(*) FROM admins").fetchone()[0] == 0:
                seed_data.seed(db)

    init_db()

    # ---------- security helpers ----------
    def login_required(view):
        """Decorator: only a logged-in admin may open the page."""
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("admin"):
                flash("Please log in to open the admin area.", "error")
                return redirect(url_for("admin_login", next=request.path))
            return view(*args, **kwargs)
        return wrapped

    def csrf_token():
        """A random value kept in the session and repeated in every form.
        A form posted from another website will not know it, so it is rejected."""
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(16)
        return session["csrf"]

    @app.before_request
    def check_csrf():
        if request.method == "POST":
            sent = request.form.get("csrf_token", "")
            if not sent or not secrets.compare_digest(sent, session.get("csrf", "")):
                abort(400, "Your form session expired. Go back, reload the page and try again.")

    @app.context_processor
    def inject_globals():
        return {"dept": DEPARTMENT, "csrf_token": csrf_token, "today": date.today().isoformat()}

    def now():
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def like(text):
        """Build a 'contains' search pattern. In SQL LIKE, % and _ are wildcards,
        so a visitor typing them must have them treated as ordinary characters
        (fix for defect D-01)."""
        escaped = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        return f"%{escaped}%"

    # ================= PUBLIC PAGES (visitor) =================
    @app.route("/")
    def home():
        db = get_db()
        latest = db.execute(
            "SELECT * FROM announcements ORDER BY published_on DESC, id DESC LIMIT 3").fetchall()
        upcoming = db.execute(
            "SELECT * FROM events WHERE event_date >= ? ORDER BY event_date, event_time LIMIT 3",
            (date.today().isoformat(),)).fetchall()
        counts = {
            "faculty": db.execute("SELECT COUNT(*) FROM faculty").fetchone()[0],
            "announcements": db.execute("SELECT COUNT(*) FROM announcements").fetchone()[0],
            "upcoming": db.execute("SELECT COUNT(*) FROM events WHERE event_date >= ?",
                                   (date.today().isoformat(),)).fetchone()[0],
        }
        return render_template("home.html", latest=latest, upcoming=upcoming, counts=counts)

    @app.route("/announcements")
    def announcements():
        q = request.args.get("q", "").strip()[:60]
        category = request.args.get("category", "").strip()
        if category not in v.CATEGORIES:
            category = ""
        sql, params = "SELECT * FROM announcements WHERE 1=1", []
        if q:
            # ? placeholders keep user text out of the SQL itself (prevents SQL injection)
            sql += " AND (title LIKE ? ESCAPE '\\' OR body LIKE ? ESCAPE '\\')"
            params += [like(q), like(q)]
        if category:
            sql += " AND category = ?"
            params.append(category)
        rows = get_db().execute(sql + " ORDER BY published_on DESC, id DESC", params).fetchall()
        return render_template("announcements.html", rows=rows, q=q, category=category,
                               categories=v.CATEGORIES)

    @app.route("/announcements/<int:item_id>")
    def announcement_detail(item_id):
        row = get_db().execute("SELECT * FROM announcements WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            abort(404)
        return render_template("announcement_detail.html", row=row)

    @app.route("/faculty")
    def faculty():
        q = request.args.get("q", "").strip()[:60]
        sql, params = "SELECT * FROM faculty", []
        if q:
            sql += (" WHERE name LIKE ? ESCAPE '\\' OR specialization LIKE ? ESCAPE '\\'"
                    " OR designation LIKE ? ESCAPE '\\'")
            params = [like(q)] * 3
        rows = get_db().execute(sql + " ORDER BY id", params).fetchall()
        return render_template("faculty.html", rows=rows, q=q)

    @app.route("/faculty/<int:item_id>")
    def faculty_detail(item_id):
        row = get_db().execute("SELECT * FROM faculty WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            abort(404)
        return render_template("faculty_detail.html", row=row)

    @app.route("/events")
    def events():
        db, today = get_db(), date.today().isoformat()
        upcoming = db.execute(
            "SELECT * FROM events WHERE event_date >= ? ORDER BY event_date, event_time",
            (today,)).fetchall()
        past = db.execute(
            "SELECT * FROM events WHERE event_date < ? ORDER BY event_date DESC", (today,)).fetchall()
        return render_template("events.html", upcoming=upcoming, past=past)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form, errors = {}, {}
        if request.method == "POST":
            form, errors = v.validate_message(request.form)
            if not errors:
                db = get_db()
                db.execute(
                    "INSERT INTO messages (name, email, subject, body, created_at) VALUES (?, ?, ?, ?, ?)",
                    (form["name"], form["email"], form["subject"], form["body"], now()))
                db.commit()
                flash("Thank you. Your message was saved and the department office can now read it.",
                      "success")
                return redirect(url_for("contact"))
            flash("Please correct the highlighted fields.", "error")
        return render_template("contact.html", form=form, errors=errors), (400 if errors else 200)

    # ================= ADMIN PAGES (content editor) =================
    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                error = "Enter both username and password."
            else:
                row = get_db().execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
                # Same message for a wrong username and a wrong password, so an
                # attacker cannot learn which usernames exist.
                if row is None or not check_password_hash(row["password_hash"], password):
                    error = "Incorrect username or password."
                else:
                    session.clear()
                    session["admin"] = row["username"]
                    flash(f"Welcome, {row['username']}.", "success")
                    target = request.args.get("next", "")
                    # Only follow `next` if it points inside our own admin area.
                    if not target.startswith("/admin"):
                        target = url_for("admin_dashboard")
                    return redirect(target)
        return render_template("admin/login.html", error=error), (401 if error else 200)

    @app.route("/admin/logout", methods=["POST"])
    def admin_logout():
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for("home"))

    @app.route("/admin")
    @login_required
    def admin_dashboard():
        db = get_db()
        data = {kind: db.execute(f"SELECT * FROM {cfg['table']} ORDER BY {cfg['order']}").fetchall()
                for kind, cfg in CONTENT.items()}
        unread = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        return render_template("admin/dashboard.html", data=data, content=CONTENT, message_count=unread)

    @app.route("/admin/messages")
    @login_required
    def admin_messages():
        rows = get_db().execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        return render_template("admin/messages.html", rows=rows)

    def validate(kind, form, existing):
        if kind == "announcements":
            return v.validate_announcement(form)
        if kind == "events":
            # An old event may keep its past date while other details are edited.
            unchanged = existing is not None and form.get("event_date", "").strip() == existing["event_date"]
            return v.validate_event(form, allow_past=unchanged)
        return v.validate_faculty(form)

    def duplicate_error(kind, clean, item_id):
        """Return (field, message) if the record would be a duplicate, else None."""
        db, skip = get_db(), item_id or 0
        if kind == "announcements":
            hit = db.execute("SELECT 1 FROM announcements WHERE title = ? AND id != ?",
                             (clean["title"], skip)).fetchone()
            return ("title", "An announcement with this title already exists.") if hit else None
        if kind == "events":
            hit = db.execute("SELECT 1 FROM events WHERE title = ? AND event_date = ? AND id != ?",
                             (clean["title"], clean["event_date"], skip)).fetchone()
            return ("title", "This event is already listed on the same date.") if hit else None
        hit = db.execute("SELECT 1 FROM faculty WHERE email = ? AND id != ?",
                         (clean["email"], skip)).fetchone()
        return ("email", "Another faculty profile already uses this email.") if hit else None

    @app.route("/admin/<kind>/new", methods=["GET", "POST"])
    @app.route("/admin/<kind>/<int:item_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_form(kind, item_id=None):
        """Create (no item_id) or update (with item_id) one record."""
        cfg = CONTENT.get(kind)
        if cfg is None:
            abort(404)
        db = get_db()
        existing = None
        if item_id is not None:
            existing = db.execute(f"SELECT * FROM {cfg['table']} WHERE id = ?", (item_id,)).fetchone()
            if existing is None:
                abort(404)

        form = dict(existing) if existing else {}
        errors = {}
        if request.method == "POST":
            form, errors = validate(kind, request.form, existing)
            if not errors:
                dup = duplicate_error(kind, form, item_id)
                if dup:
                    errors[dup[0]] = dup[1]
            if not errors:
                cols = cfg["columns"]
                values = [form[c] for c in cols]
                extra = [] if kind == "faculty" else ["updated_at"]
                if kind != "faculty":
                    values.append(now())
                try:
                    if existing:
                        assignments = ", ".join(f"{c} = ?" for c in cols + extra)
                        db.execute(f"UPDATE {cfg['table']} SET {assignments} WHERE id = ?",
                                   values + [item_id])
                    else:
                        names = ", ".join(cols + extra)
                        marks = ", ".join("?" for _ in cols + extra)
                        db.execute(f"INSERT INTO {cfg['table']} ({names}) VALUES ({marks})", values)
                    db.commit()
                except sqlite3.IntegrityError:
                    # Safety net: the UNIQUE rule in the database caught a duplicate
                    # that slipped past the check above (two editors saving at once).
                    db.rollback()
                    errors[cfg["name_column"]] = "This record already exists."
                else:
                    action = "updated" if existing else "created"
                    flash(f"{cfg['label']} {action}: {form[cfg['name_column']]}", "success")
                    return redirect(url_for("admin_dashboard") + f"#{kind}")
            flash("Nothing was saved. Please correct the highlighted fields.", "error")
        return render_template("admin/form.html", cfg=cfg, kind=kind, form=form, errors=errors,
                               editing=existing is not None), (400 if errors else 200)

    @app.route("/admin/<kind>/<int:item_id>/delete", methods=["POST"])
    @login_required
    def admin_delete(kind, item_id):
        cfg = CONTENT.get(kind)
        if cfg is None:
            abort(404)
        db = get_db()
        row = db.execute(f"SELECT * FROM {cfg['table']} WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            abort(404)
        db.execute(f"DELETE FROM {cfg['table']} WHERE id = ?", (item_id,))
        db.commit()
        flash(f"{cfg['label']} deleted: {row[cfg['name_column']]}", "success")
        return redirect(url_for("admin_dashboard") + f"#{kind}")

    # ================= ERROR PAGES =================
    def error_page(code, title, message):
        return render_template("error.html", code=code, title=title, message=message), code

    @app.errorhandler(400)
    def bad_request(e):
        return error_page(400, "Request could not be processed", e.description)

    @app.errorhandler(404)
    def not_found(_e):
        return error_page(404, "Page not found",
                          "The page or record you asked for does not exist or was removed.")

    @app.errorhandler(405)
    def wrong_method(_e):
        return error_page(405, "Action not allowed", "This address cannot be used that way.")

    @app.errorhandler(413)
    def too_large(_e):
        return error_page(413, "Submission too large", "Please shorten the text and try again.")

    @app.errorhandler(500)
    def server_error(_e):
        return error_page(500, "Something went wrong",
                          "An unexpected error occurred. Your data was not changed. Please try again.")

    return app


# Vercel imports this file and serves the top-level object named `app`.
# Locally it stays empty so that importing this file never touches the database.
app = create_app() if ON_VERCEL else None

if __name__ == "__main__":
    db_file = DEFAULT_DB
    if "--reset" in sys.argv and os.path.exists(db_file):
        os.remove(db_file)
        print("Database reset. Sample data reloaded.")
    create_app().run(debug=False, port=5000)
