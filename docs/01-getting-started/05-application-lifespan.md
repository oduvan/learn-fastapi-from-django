# Application lifespan

Some work happens once per process, not once per request: opening a
database connection pool, creating a shared HTTP client, loading an ML
model or a config file into memory, and tearing those down cleanly on the
way out. FastAPI puts this in a **lifespan** — an async context manager
tied to the server's startup and shutdown.

## The `lifespan` context manager

Write an `@asynccontextmanager` function that takes the app. Everything
before `yield` runs **once at startup**, before any request is served;
everything after `yield` runs **once at shutdown**, after the last request.
Pass it to `FastAPI(lifespan=...)`:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.db import FakePool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = FakePool()   # startup: open the resource
    yield
    app.state.pool.close()        # shutdown: close it


app = FastAPI(lifespan=lifespan)


@app.get("/users")
def list_users(request: Request):
    return {"users": request.app.state.pool.get_users()}
```

The resource lives on `app.state` — a plain namespace for
application-wide objects — and endpoints reach it through
`request.app.state`. Start the app and Uvicorn logs `Application startup
complete` once the startup half has run; on Ctrl-C it runs the shutdown
half before exiting.

Because it's a single context manager, setup and teardown sit next to each
other and share scope — the `try/finally` shape of "acquire, yield, release"
that Python context managers are built for.

!!! note
    The older `@app.on_event("startup")` / `@app.on_event("shutdown")`
    decorators still exist but are deprecated. Use `lifespan` for new code.

## Getting at the resource

Two ways to use what lifespan created:

- `request.app.state.pool` — directly, as above.
- A **dependency** that returns `request.app.state.pool`, so endpoints ask
  for `pool` in their signature instead of reaching through the request.
  That's the idiomatic approach and gets its own topic (Dependency
  injection).

> **From Django:** The closest thing Django gives you is
> `AppConfig.ready()` — a method that runs once, when the app registry
> finishes loading. It's where you register signals, run startup checks, or
> warm a cache. Two differences matter:
>
> **It's startup-only.** There is no `ready()` counterpart for shutdown —
> Django has no built-in process-shutdown hook for your code. FastAPI's
> lifespan is symmetric: the same function owns both ends, so the thing you
> open you also close.
>
> **It runs almost everywhere.** `ready()` fires for *every* entry point
> that loads the app registry — `runserver`, but also every `manage.py`
> command, migrations, and the shell. That's why you're warned not to do
> heavy work (like opening real connections) in `ready()` without guarding
> it. FastAPI's `lifespan` runs only when the ASGI app is actually served
> by Uvicorn — not when you import a module or run a one-off script — so
> "open a connection pool here" is exactly what it's for.

## The companion projects make the asymmetry concrete

The FastAPI project opens the pool at startup and **closes it at
shutdown**, and its test asserts both halves. The Django project opens the
same pool in `AppConfig.ready()` and has **no shutdown step** — because
there's nowhere to put one. Same startup resource, but only one framework
gives you the matching teardown.

## Testing note

`TestClient` runs the lifespan **only when used as a context manager**:

```python
with TestClient(app) as client:   # startup runs here
    ...                           # make requests
# shutdown runs here, on exit
```

A module-level `client = TestClient(app)` skips lifespan entirely — so an
endpoint relying on `app.state.pool` would fail. This trips people up; when
your tests touch lifespan-created state, use the `with` form.

## Companion projects { #companion-projects }

Under this chapter's `05-demo/` folder:

- `05-demo/fastapi/` ([download](05-demo-fastapi.zip)) — a `lifespan` that
  opens and closes the pool; test asserts open-during, closed-after.
- `05-demo/django/` ([download](05-demo-django.zip)) — `AppConfig.ready()`
  opens the pool; test asserts it's open at startup (no shutdown to test).

FastAPI: `pytest` (2 tests). Django: `manage.py test` (3 tests).

## Sources

- [FastAPI — Lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [Starlette — Lifespan](https://www.starlette.io/lifespan/)
- [Django — `AppConfig.ready()`](https://docs.djangoproject.com/en/6.0/ref/applications/#django.apps.AppConfig.ready)
- [Django — Applications registry](https://docs.djangoproject.com/en/6.0/ref/applications/)
