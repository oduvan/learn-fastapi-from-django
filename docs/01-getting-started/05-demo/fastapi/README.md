# Application Lifespan — FastAPI

Companion project for *Getting started → Application lifespan*. A `lifespan`
context manager opens a resource (a fake connection pool) at startup and
closes it at shutdown; an endpoint uses it via `request.app.state`.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/fastapi dev app/main.py
# or: .venv/bin/uvicorn app.main:app --reload
```

Watch the logs: Uvicorn prints "Application startup complete" once the
lifespan startup has run.

## Test

```bash
.venv/bin/pytest
```

The test uses `TestClient` **as a context manager** (`with TestClient(app)
as client:`) — that's what makes the lifespan run in tests. It asserts the
pool is open inside the block and closed after it.

## Endpoints

| Method & path | Response |
|---|---|
| `GET /users` | `{"users": [...]}` (served from the startup-opened pool) |
| `GET /health` | `{"status": "ok"}` |
