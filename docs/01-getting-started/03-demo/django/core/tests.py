import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from django.test import TestCase

# Project root — the directory that holds manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent


class ViewTests(TestCase):
    def test_root(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "It works!"})

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class RunserverTests(TestCase):
    """Boot the real `manage.py runserver` and hit it over HTTP."""

    def test_runserver_serves_over_http(self):
        port = _free_port()
        proc = subprocess.Popen(
            [sys.executable, "manage.py", "runserver",
             f"127.0.0.1:{port}", "--noreload"],
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 20
            last_err = None
            while time.monotonic() < deadline:
                try:
                    with urllib.request.urlopen(
                        f"http://127.0.0.1:{port}/health", timeout=1
                    ) as r:
                        self.assertEqual(r.status, 200)
                        self.assertEqual(
                            json.loads(r.read()), {"status": "ok"}
                        )
                        return
                except Exception as exc:  # not ready yet
                    last_err = exc
                    time.sleep(0.3)
            self.fail(f"runserver did not become ready: {last_err}")
        finally:
            proc.terminate()
            proc.wait(timeout=10)
