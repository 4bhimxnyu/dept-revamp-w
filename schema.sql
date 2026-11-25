-- Database design for the Department Website.
-- Five tables. SQLite stores them in one file (department.db).

CREATE TABLE IF NOT EXISTS admins (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL            -- never the plain password
);

CREATE TABLE IF NOT EXISTS announcements (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT NOT NULL UNIQUE COLLATE NOCASE,  -- no two with the same title
    category     TEXT NOT NULL,
    body         TEXT NOT NULL,
    published_on TEXT NOT NULL,            -- YYYY-MM-DD
    updated_at   TEXT NOT NULL             -- YYYY-MM-DD HH:MM
);

CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL COLLATE NOCASE,
    event_date  TEXT NOT NULL,             -- YYYY-MM-DD
    event_time  TEXT NOT NULL,             -- HH:MM (24 hour)
    venue       TEXT NOT NULL,
    description TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    UNIQUE (title, event_date)             -- same event cannot be added twice on one day
);

CREATE TABLE IF NOT EXISTS faculty (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    designation    TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE COLLATE NOCASE,
    phone          TEXT NOT NULL,
    qualification  TEXT NOT NULL,
    specialization TEXT NOT NULL,
    bio            TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    subject    TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL
);
