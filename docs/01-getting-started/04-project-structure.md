# Project structure

FastAPI does not prescribe a project layout. There is no `startproject`, no
`settings.py`, no notion of "apps" you register. A project can be one
`main.py` file, and grow into a package when that file gets too big. This
chapter shows how it grows — and how that maps to Django's project/app
split.

## The one tool: `APIRouter`

As soon as one file is too much, you split routes into **routers**. An
`APIRouter` is a mini-collection of path operations you build in its own
module and then attach to the app:

```python
# app/routers/items.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/items", tags=["items"])

ITEMS = [{"id": 1, "name": "Widget"}, {"id": 2, "name": "Gadget"}]


@router.get("")
def list_items():
    return {"items": ITEMS}


@router.get("/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
```

`APIRouter` behaves like `FastAPI` for declaring routes — same
`@router.get(...)` decorators — but it doesn't serve anything on its own.
You wire it into the application with `include_router`:

```python
# app/main.py
from fastapi import FastAPI

from app.routers import items, users

app = FastAPI(title="Project Structure (FastAPI)")

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "It works!"}
```

The `prefix="/items"` on the router means its routes live under `/items`
(`""` → `/items`, `/{item_id}` → `/items/{item_id}`). `tags=["items"]`
groups them in the `/docs` UI. That's the whole mechanism: build routers in
modules, `include_router` them in `main.py`.

> **From Django:** `include_router(items.router)` is the direct analogue of
> `path("", include("items.urls"))`. An `APIRouter` with a `prefix` is
> essentially an app's `urls.py` with its URL prefix attached. But that's
> *all* it is — a group of routes. A Django **app** is much more: a bundle
> of `models.py`, migrations, `admin.py`, templates, and `urls.py`
> registered in `INSTALLED_APPS`. A router carries none of that. So one
> Django app usually becomes, on the FastAPI side, *just* a router module
> (plus separate modules for whatever models/schemas/dependencies you add
> later).

## A layout that scales

The community-standard shape for a growing app is a package with a
`routers/` (or `routers`/`api`) subpackage:

```
app/
├── __init__.py
├── main.py            # creates FastAPI(), includes the routers
└── routers/
    ├── __init__.py
    ├── items.py       # APIRouter(prefix="/items")
    └── users.py       # APIRouter(prefix="/users")
```

Run it with `fastapi dev app/main.py` (or `uvicorn app.main:app --reload`).
As the project grows you add sibling modules — `models.py`, `schemas.py`,
`dependencies.py`, `database.py`, `config.py` — wherever you decide they
belong. Nothing enforces these names; they're conventions, not framework
rules.

> **From Django:** Two habits to unlearn.
>
> First, **there is no `INSTALLED_APPS` and no app registry.** Nothing is
> auto-discovered. `main.py` imports each router and calls `include_router`
> explicitly — what you import is what runs. There's no `apps.py`,
> no `AppConfig`, no `ready()` hook, no app-loading phase.
>
> Second, **the project/app distinction doesn't exist.** Django gives you a
> project (`config/`) that owns settings and the root URLconf, and apps
> that plug into it. FastAPI has just "your code": the `FastAPI()` instance
> and whatever modules you import into it. `main.py` plays the combined
> role of `settings.py`'s wiring and the root `urls.py`, but you assemble
> it by hand.

## Routers do a bit more than group URLs

An `APIRouter` can also attach a `prefix`, `tags`, `dependencies`, and
default `responses` to every route it holds, and routers can include other
routers — so you can build a tree (`/api/v1/items`) by nesting them:

```python
api = APIRouter(prefix="/api/v1")
api.include_router(items.router)     # -> /api/v1/items
api.include_router(users.router)     # -> /api/v1/users
app.include_router(api)
```

> **From Django:** Nesting routers to build `/api/v1/...` is what nested
> `include()` calls do in Django URLconfs. Router-level `dependencies=[...]`
> (every route in the router runs them) is the rough analogue of wrapping
> an app's views in middleware or a common decorator — but scoped to the
> router, and covered properly in the Dependency injection topic.

## Companion projects { #companion-projects }

The layout above, built both ways, under this chapter's `04-demo/` folder:

- `04-demo/fastapi/` ([download](04-demo-fastapi.zip)) — an `app/` package
  with `routers/items.py` and `routers/users.py` wired in `app/main.py`.
- `04-demo/django/` ([download](04-demo-django.zip)) — a `config/` project
  with `items/` and `users/` apps, each `include()`d in `config/urls.py`.

Both expose the same `/items` and `/users` API; their tests assert the
same responses. FastAPI: `pytest` (7 tests). Django: `manage.py test`
(6 tests, split across the two apps).

## Sources

- [FastAPI — Bigger Applications, multiple files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI — APIRouter reference](https://fastapi.tiangolo.com/reference/apirouter/)
- [Django — URL dispatcher, `include()`](https://docs.djangoproject.com/en/6.0/ref/urls/#include)
- [Django — Applications and the app registry](https://docs.djangoproject.com/en/6.0/ref/applications/)
