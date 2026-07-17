# First App — FastAPI

Companion project for *Getting started → Installing FastAPI and your first
app*. A tiny read-only API over an in-memory list of items.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --reload
# http://127.0.0.1:8000  ·  interactive docs at http://127.0.0.1:8000/docs
```

## Test

```bash
.venv/bin/pytest
```

## Endpoints

| Method & path | Response |
|---|---|
| `GET /` | `{"message": "It works!"}` |
| `GET /items` | `{"items": [...]}` (accepts `?limit=`) |
| `GET /items/{item_id}` | one item, or `404 {"detail": "Item not found"}` |

`GET /items/abc` returns `422` — FastAPI validates the path type before
your function runs.
