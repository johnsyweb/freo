from app import app


def test_get_root_returns_hello_world_page():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    assert b"<h1>Hello, World</h1>" in response.data


def test_unknown_path_returns_404():
    response = app.test_client().get("/nope")

    assert response.status_code == 404
