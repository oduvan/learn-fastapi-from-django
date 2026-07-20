# Project Structure — FastAPI

Companion project for *Getting started → Project structure*. A small app
split into an `app/` package with one `APIRouter` per resource, wired
together in `app/main.py` with `include_router`.

```
app/
├── __init__.py
├── main.py            # creates FastAPI(), includes the routers
└── routers/
    ├── __init__.py
    ├── items.py       # APIRouter(prefix="/items")
    └── users.py       # APIRouter(prefix="/users")
```

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/fastapi dev app/main.py
# or: .venv/bin/uvicorn app.main:app --reload
```

## Test

```bash
.venv/bin/pytest
```

## Endpoints

| Method & path | Response |
|---|---|
| `GET /` | `{"message": "It works!"}` |
| `GET /items` · `GET /items/{id}` | items list · one item / `404` |
| `GET /users` · `GET /users/{id}` | users list · one user / `404` |
