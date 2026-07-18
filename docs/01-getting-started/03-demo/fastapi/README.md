# Dev Server — FastAPI

Companion project for *Getting started → The dev server*. A minimal app
used to demonstrate the ways of running FastAPI in development.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# The fastapi[standard] CLI — auto-reload, binds 127.0.0.1:8000, prints /docs:
.venv/bin/fastapi dev main.py

# The underlying Uvicorn command (equivalent):
.venv/bin/uvicorn main:app --reload

# Choose host/port:
.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 9000

# Production-style (no reload, binds 0.0.0.0, multiple workers):
.venv/bin/fastapi run main.py --workers 4
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Test

```bash
.venv/bin/pytest
```

One test boots the real Uvicorn server in a subprocess and hits it over
HTTP, so it exercises the actual ASGI server — not just `TestClient`.

## Endpoints

| Method & path | Response |
|---|---|
| `GET /` | `{"message": "It works!"}` |
| `GET /health` | `{"status": "ok"}` |
