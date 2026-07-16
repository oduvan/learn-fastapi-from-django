# What is FastAPI

FastAPI is a Python web framework for building APIs, created by Sebastián
Ramírez and first released in December 2018. It is open source under the
MIT license. Its selling points are that you declare your API with
ordinary **Python type hints**, and in return you get automatic request
validation, serialization, and interactive API documentation — with
performance on par with Node.js and Go, because it runs on **ASGI**
(async) rather than WSGI (sync).

If you come from Django, the single most important thing to understand up
front is this: **FastAPI is not a Django-sized framework.** It is a thin,
focused layer that does routing, validation, and documentation, and
leaves everything else — the database, the admin, templates, auth — to
libraries you choose and wire together yourself.

## FastAPI is a stack, not a monolith

Installing Django gives you one coherent thing that does almost
everything. FastAPI is deliberately small and stands on two other
libraries:

- **[Starlette](https://www.starlette.io/)** — the ASGI toolkit
  underneath. It provides the actual HTTP handling: routing, requests and
  responses, middleware, background tasks, WebSockets, and the test
  client. FastAPI *is* a Starlette application with extra features layered
  on top. Anything Starlette can do, a FastAPI app can do.
- **[Pydantic](https://docs.pydantic.dev/)** — data validation and
  serialization from type hints. Every request body, query parameter, and
  response shape is a Pydantic model or a type Pydantic understands.

FastAPI itself contributes the type-hint magic that ties these together:
it reads your function signatures, wires up validation via Pydantic and
routing via Starlette, and generates an **OpenAPI** schema for free.

To actually serve requests you also need an **ASGI server** — most
commonly **[Uvicorn](https://www.uvicorn.org/)**. That's the equivalent
of the WSGI server (Gunicorn/uWSGI) you already run Django behind in
production, except it speaks the async ASGI protocol.

> **From Django:** Django is "batteries included" — ORM, migrations,
> admin, auth, forms, templates, sessions, and the WSGI handler all ship
> in one package with one release cycle. FastAPI is the opposite: it owns
> routing + validation + docs, and for everything else you assemble a
> stack. There is no `django-admin startproject` that lays down a
> settings module, a URL conf, and a WSGI entry point. You start from an
> empty file.

## What ships, and what you bring yourself

| Concern | Django | FastAPI |
|---|---|---|
| URL routing | `urls.py` + `path()` | decorators on functions (`@app.get(...)`) |
| Request validation | Forms / DRF serializers | Pydantic models (built in) |
| Serialization | DRF serializers / templates | Pydantic + `response_model` (built in) |
| Interactive API docs | DRF Browsable API / add-on | Swagger UI + ReDoc (built in) |
| ORM | Django ORM (built in) | none — bring SQLAlchemy, SQLModel, Tortoise, … |
| Migrations | Django migrations (built in) | none — bring Alembic (or your ORM's tool) |
| Admin site | `django.contrib.admin` (built in) | none — bring SQLAdmin, Piccolo, or build one |
| Auth / sessions | `django.contrib.auth` (built in) | none — bring OAuth2/JWT helpers, `Depends` |
| Templates | Django Template Language (built in) | none built in — Starlette + Jinja2 |
| Settings | `settings.py` module | none — bring `pydantic-settings` |
| Server | WSGI (ASGI optional) | ASGI (Uvicorn) |

The empty cells on the FastAPI side are the whole reason this book has a
"From Django's batteries to a FastAPI stack" topic near the end: moving
to FastAPI is partly learning the framework and partly learning which
library replaces each Django battery you took for granted.

## The type-hint idea in 10 lines

Here is a complete FastAPI application. It validates input, serializes
output, and documents itself — all from the type hints.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

From those hints FastAPI infers that:

- `item_id` comes from the path and must be an `int` — `/items/abc`
  returns a `422` validation error, not a crash.
- `q` is an optional query string — `/items/5?q=hello` works, so does
  `/items/5`.
- the returned `dict` is serialized to JSON.

Run it with Uvicorn and open `/docs`:

```bash
pip install "fastapi[standard]==0.139.2" "uvicorn==0.34.0"
uvicorn main:app --reload
# open http://127.0.0.1:8000/docs
```

You get a live Swagger UI where you can call the endpoint, plus a second
docs UI at `/redoc`, both generated from the same OpenAPI schema.

> **From Django:** The closest Django-world analogue is Django REST
> Framework, where you declare a `Serializer` and get validation plus a
> Browsable API. FastAPI collapses that into the function signature
> itself — the parameter *is* the schema. And where DRF's schema/OpenAPI
> generation is an add-on you configure, in FastAPI the OpenAPI document
> and the two doc UIs are on by default from the first line.

## ASGI vs WSGI: why "async" is the headline

WSGI — the protocol Django was built on — is synchronous: one request
occupies one worker thread/process until it finishes. ASGI is the async
successor. It lets a single worker handle many in-flight requests
concurrently by suspending them at `await` points (waiting on a database,
an HTTP call, a queue) instead of blocking a whole thread.

FastAPI is ASGI-native. You write path operations as either `def`
(regular, run in a threadpool) or `async def` (run on the event loop),
and mixing them is fine:

```python
@app.get("/sync")
def sync_view():
    return {"style": "sync"}


@app.get("/async")
async def async_view():
    return {"style": "async"}
```

> **From Django:** Django is WSGI-first but has supported ASGI and
> `async def` views for several versions, so async isn't unique to
> FastAPI. The practical difference is default and depth: FastAPI is
> async all the way down (Starlette, the test client, dependencies,
> middleware), whereas in Django large parts of the stack — most notably
> much of the ORM — are still synchronous, so an `async def` view often
> ends up calling `sync_to_async` around blocking pieces. We devote a
> whole topic to this later.

## Stewardship, versioning, and stability

- Developed in the open at
  [github.com/fastapi/fastapi](https://github.com/fastapi/fastapi).
- MIT licensed; primarily maintained by Sebastián Ramírez and a team of
  maintainers, funded through sponsorships.
- **Pre-1.0.** FastAPI is versioned `0.x`. In practice it is widely used
  in production and quite stable, but it does **not** follow semantic
  versioning yet: a minor version bump (e.g. `0.138` → `0.139`) can
  include a breaking change. **Pin an exact version** (`fastapi==0.139.2`)
  and read the release notes before upgrading.

> **From Django:** This is a real culture shift. Django's Sixth-release
> compatibility guarantees and LTS branches mean you can lean on a
> version for years. FastAPI moves faster and asks you to pin and track
> more actively — and because your stack is several independently
> versioned libraries (FastAPI, Starlette, Pydantic, Uvicorn, your ORM),
> "the framework version" is really a set of versions you manage together.

## Community and resources

- **[fastapi.tiangolo.com](https://fastapi.tiangolo.com/)** — the
  official docs; the tutorial is excellent and doubles as a reference.
- **[docs.pydantic.dev](https://docs.pydantic.dev/)** and
  **[starlette.io](https://www.starlette.io/)** — you will read these
  directly, since FastAPI hands real work to both.
- The FastAPI GitHub Discussions, the `r/FastAPI` subreddit, and the
  large Pydantic/SQLAlchemy communities you'll draw the rest of your
  stack from.

## Sources

- [FastAPI — official site](https://fastapi.tiangolo.com/)
- [FastAPI — Features](https://fastapi.tiangolo.com/features/)
- [FastAPI on GitHub](https://github.com/fastapi/fastapi)
- [Starlette — official site](https://www.starlette.io/)
- [Pydantic — documentation](https://docs.pydantic.dev/latest/)
- [Uvicorn — an ASGI web server](https://www.uvicorn.org/)
- [ASGI specification](https://asgi.readthedocs.io/en/latest/)
- [Django — Async support](https://docs.djangoproject.com/en/6.0/topics/async/)
