"""Shared test setup. Each test gets a brand new temporary database,
so tests never affect each other or the real department.db."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from seed import DEMO_ADMIN  # noqa: E402


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def token(client):
    """Open a page so the session gets a CSRF token, then read it back."""
    client.get("/contact")
    with client.session_transaction() as s:
        return s["csrf"]


def post(client, url, data, **kwargs):
    """POST a form with a valid CSRF token, like a real browser would."""
    return client.post(url, data={**data, "csrf_token": token(client)}, **kwargs)


@pytest.fixture
def admin(client):
    """A client that is already logged in as the demo admin."""
    response = post(client, "/admin/login", {"username": DEMO_ADMIN[0], "password": DEMO_ADMIN[1]})
    assert response.status_code == 302
    return client
