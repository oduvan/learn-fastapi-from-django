# First App — Django

Companion project for *Getting started → Installing FastAPI and your first
app*. The same read-only API as the FastAPI project, built the Django way:
a project (`config/`) plus one app (`items/`) with function views that
return `JsonResponse`.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py runserver
# http://127.0.0.1:8000
```

## Test

```bash
.venv/bin/python manage.py test
```

## Endpoints

| Method & path | Response |
|---|---|
| `GET /` | `{"message": "It works!"}` |
| `GET /items` | `{"items": [...]}` (reads `?limit=` from `request.GET`) |
| `GET /items/{item_id}` | one item, or `404 {"detail": "Item not found"}` |

`GET /items/abc` returns `404` — the `<int:item_id>` URL converter doesn't
match a non-integer, so the resolver never reaches the view. (The FastAPI
version returns `422` instead: same intent, different mechanism.)
