from app import app
import app as app_module


def test_get_root_returns_hello_world_page():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    assert b"<h1>Hello, World</h1>" in response.data


def test_get_root_states_the_operating_system_and_version(monkeypatch):
    monkeypatch.setattr(
        app_module, "operating_system_description", lambda: "TestOS 1.0"
    )

    response = app.test_client().get("/")

    assert (
        b"<p>The underlying operating system is TestOS 1.0.</p>" in response.data
    )


def test_get_root_states_the_host_time_in_utc(monkeypatch):
    monkeypatch.setattr(
        app_module, "host_time_description", lambda: "2026-08-29T06:50:00Z"
    )

    response = app.test_client().get("/")

    assert (
        b"<p>The time on this host is 2026-08-29T06:50:00Z (UTC).</p>"
        in response.data
    )


def test_unknown_path_returns_404():
    response = app.test_client().get("/nope")

    assert response.status_code == 404
