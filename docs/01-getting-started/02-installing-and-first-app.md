# Installing FastAPI and your first app

This chapter gets a FastAPI app running and builds the same small API two
ways — once in FastAPI, once in Django — so the shape of the difference is
concrete from the start. Both versions ship as
[companion projects](#companion-projects) you can run and test.

## Installing

FastAPI is a normal PyPI package. Create a virtual environment and install
it — the `[standard]` extra pulls in the pieces you'll actually want in
development (the Uvicorn server, the `fastapi` CLI, `httpx` for the test
client, Jinja2, and form/file support):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "fastapi[standard]==0.139.2"
```

That's the whole install. There is no `startproject`, no `settings.py`, no
generated directory tree — you create an empty `.py` file and start
writing.

> **From Django:** `pip install Django` then `django-admin startproject
> config .` scaffolds a project package (`settings.py`, `urls.py`,
> `wsgi.py`, `asgi.py`) and a `manage.py`. FastAPI scaffolds nothing. The
> upside is zero ceremony; the downside is that structure, settings, and
> entry points are decisions you make yourself (topic 1 has a whole chapter
> on project layout).

## Your first app

Put this in `main.py`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI(title="First App (FastAPI)")

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


@app.get("/")
def read_root():
    return {"message": "It works!"}


@app.get("/items")
def list_items(limit: int = 10):
    return {"items": ITEMS[:limit]}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
```

Three things are happening, all driven by the function signatures:

- **Routing is a decorator.** `@app.get("/items")` binds a path and HTTP
  method directly to the function. There is no separate URL table.
- **Return a `dict`, get JSON.** FastAPI serializes the return value and
  sets `content-type: application/json`. You don't touch a response object
  for the common case.
- **Parameters are typed and validated.** `item_id: int` means the path
  segment is parsed and validated as an integer; `limit: int = 10` becomes
  an optional query parameter with a default.

### Run it

```bash
fastapi dev main.py          # the fastapi[standard] CLI, with auto-reload
# or, equivalently:
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/items>, then <http://127.0.0.1:8000/docs> for
the interactive Swagger UI that FastAPI generated from those same
signatures.

> **From Django:** `fastapi dev main.py` is the `manage.py runserver` of
> this world — a dev server with auto-reload. The difference underneath:
> `runserver` is a WSGI dev server, while Uvicorn is an ASGI server, and
> the `/docs` UI has no `runserver` equivalent — you'd reach for DRF's
> Browsable API or `drf-spectacular` to get something comparable.

## The same API in Django

Here is the identical API built with Django views. Django needs a project
package, an app, a URL table, and views that return `JsonResponse`:

```python
# config/urls.py
from django.urls import path
from items import views

urlpatterns = [
    path("", views.read_root),
    path("items", views.list_items),
    path("items/<int:item_id>", views.get_item),
]
```

```python
# items/views.py
from django.http import JsonResponse

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


def read_root(request):
    return JsonResponse({"message": "It works!"})


def list_items(request):
    limit = int(request.GET.get("limit", 10))  # convert/validate by hand
    return JsonResponse({"items": ITEMS[:limit]})


def get_item(request, item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return JsonResponse(item)
    return JsonResponse({"detail": "Item not found"}, status=404)
```

Line them up and the division of labour is clear:

| | FastAPI | Django |
|---|---|---|
| Bind URL → handler | `@app.get("/items")` decorator | entry in `urlpatterns` |
| Read a query param | `limit: int = 10` (parsed + validated) | `int(request.GET.get("limit", 10))` (manual) |
| Return JSON | `return {...}` | `return JsonResponse({...})` |
| Signal "not found" | `raise HTTPException(404, ...)` | `JsonResponse({...}, status=404)` |
| Interactive docs | built in at `/docs` | not built in |

## One difference worth noticing now: bad input

Request `/items/abc` — a non-integer where an integer id is expected — and
the two frameworks diverge:

```http
GET /items/abc

# FastAPI → 422 Unprocessable Entity
#   {"detail":[{"type":"int_parsing","loc":["path","item_id"], ...}]}

# Django  → 404 Not Found
```

FastAPI declares `item_id: int`, so it *validates* the path and returns a
structured `422` describing what was wrong. Django's `<int:item_id>` URL
converter simply doesn't match a non-integer, so the resolver falls
through to a `404` — the view never runs. Same intent (reject bad input),
different mechanism and different status code. Both companion projects have
a test pinning this exact behaviour.

> **From Django:** In DRF you'd get FastAPI-style `400/422` validation
> errors from a serializer, but plain Django leaves per-parameter
> validation to you — the `int()` call in `list_items` above would raise
> `ValueError` (a `500`) on `?limit=abc`. FastAPI's "the type hint is the
> validation" model is closer to DRF than to Django views, but it's built
> into the function signature rather than a separate serializer class.

## Companion projects { #companion-projects }

Both apps above are complete, runnable projects under this chapter's
`02-demo/` folder:

- `02-demo/fastapi/` — `main.py`, tests, `requirements.txt`. Run with
  `fastapi dev main.py`; test with `pytest`.
- `02-demo/django/` — `config/` project + `items/` app. Run with
  `python manage.py runserver`; test with `python manage.py test`.

Each side has a small test suite (six tests) asserting the responses shown
here, including the `422`/`404` difference. Every chapter from here on
ships a pair like this.

## Sources

- [FastAPI — First steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI — Path parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/)
- [Uvicorn — deployment/running](https://www.uvicorn.org/)
- [Django — Writing your first Django app, part 1](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django — URL dispatcher (path converters)](https://docs.djangoproject.com/en/6.0/topics/http/urls/)
- [Django — JsonResponse](https://docs.djangoproject.com/en/6.0/ref/request-response/#jsonresponse-objects)
