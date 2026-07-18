import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "It works!"}


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_app_serves_over_http_via_uvicorn():
    """Boot the real Uvicorn server (not TestClient) and hit it over HTTP."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--port", str(port), "--log-level", "warning"],
        cwd=os.path.dirname(__file__) or ".",
    )
    try:
        deadline = time.monotonic() + 15
        last_err = None
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/health", timeout=1
                ) as r:
                    assert r.status == 200
                    assert json.loads(r.read()) == {"status": "ok"}
                    return
            except Exception as exc:  # not ready yet
                last_err = exc
                time.sleep(0.2)
        raise AssertionError(f"server did not become ready: {last_err}")
    finally:
        proc.terminate()
        proc.wait(timeout=10)
