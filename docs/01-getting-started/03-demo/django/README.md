# Dev Server — Django

Companion project for *Getting started → The dev server*. The same minimal
API as the FastAPI project, used to demonstrate `manage.py runserver`.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# The Django development server (auto-reload, binds 127.0.0.1:8000):
.venv/bin/python manage.py runserver

# Choose host/port:
.venv/bin/python manage.py runserver 0.0.0.0:9000

# Disable the auto-reloader:
.venv/bin/python manage.py runserver --noreload
```

`runserver` is for development only — never run it in production.

## Test

```bash
.venv/bin/python manage.py test
```

One test (`LiveServerTests`) starts a real server and hits it over HTTP.

## Endpoints

| Method & path | Response |
|---|---|
| `GET /` | `{"message": "It works!"}` |
| `GET /health` | `{"status": "ok"}` |
