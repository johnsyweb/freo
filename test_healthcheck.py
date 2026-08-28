from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.error import HTTPError, URLError

import pytest

import healthcheck


class _OkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        del format, args


class _ErrorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(500)
        self.end_headers()

    def log_message(self, format, *args):
        del format, args


def _serve(handler):
    server = HTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_healthcheck_succeeds_when_root_returns_200(monkeypatch):
    server = _serve(_OkHandler)
    monkeypatch.setenv("PORT", str(server.server_address[1]))

    healthcheck.main()

    server.shutdown()


def test_healthcheck_fails_when_root_returns_an_error(monkeypatch):
    server = _serve(_ErrorHandler)
    monkeypatch.setenv("PORT", str(server.server_address[1]))

    with pytest.raises(HTTPError):
        healthcheck.main()

    server.shutdown()


def test_healthcheck_fails_when_nothing_is_listening(monkeypatch):
    monkeypatch.setenv("PORT", "1")

    with pytest.raises(URLError):
        healthcheck.main()
