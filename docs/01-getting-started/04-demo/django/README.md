# Project Structure — Django

Companion project for *Getting started → Project structure*. The same API
as the FastAPI project, laid out the Django way: a `config/` project plus
one app per resource, each with its own `urls.py` wired in via `include()`.

```
config/            # the project (settings, root urls, wsgi/asgi)
items/             # app: models-free, just views + urls + tests
users/             # app: same shape
manage.py
```

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
| `GET /` | `{"message": "It works!"}` |
| `GET /items` · `GET /items/{id}` | items list · one item / `404` |
| `GET /users` · `GET /users/{id}` | users list · one user / `404` |
