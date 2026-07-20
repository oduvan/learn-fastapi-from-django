# Application Lifespan — Django

Companion project for *Getting started → Application lifespan*. Django's
closest analogue to FastAPI's `lifespan` is `AppConfig.ready()`, which runs
once at startup. It opens the same fake pool and stores it in a
module-level global; a view reads from it.

There is **no shutdown counterpart** — Django has no built-in
process-shutdown hook for application code. That asymmetry is the point of
the comparison.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py runserver
```

## Test

```bash
.venv/bin/python manage.py test
```

## Endpoints

| Method & path | Response |
|---|---|
| `GET /users` | `{"users": [...]}` (served from the pool opened in `ready()`) |
| `GET /health` | `{"status": "ok"}` |
