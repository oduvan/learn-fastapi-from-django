# Learn FastAPI from Django

A personal, opinionated set of conspect notes for a **Django developer
moving to FastAPI**. Every topic explains FastAPI on its own terms and
then puts it **side by side with Django**, so years of Django experience
transfer instead of getting in the way.

All material targets **FastAPI 0.139**, **Django 6.0**, and
**Python 3.13** (with **Pydantic v2**, **Starlette**, and **Uvicorn**
as the FastAPI stack).

## Who this is for

You know Django well — models and migrations, the ORM and `QuerySet`,
the admin, DRF serializers, class-based views, middleware, `settings.py`.
You do **not** know FastAPI yet. This book assumes exactly that: it never
explains what a migration is, but it explains every FastAPI, Starlette,
and Pydantic concept from zero, and each article ends by mapping it back
to what you already do in Django.

## How the notes are organised

Each topic is a numbered folder. Inside each folder, conspects and
runnable examples share one numeric sequence so the reading order is
always obvious. The Django comparison lives in `> **From Django:**`
callouts and side-by-side code, not in a separate chapter.

### [Getting started](01-getting-started/01-what-is-fastapi.md)

- [What is FastAPI](01-getting-started/01-what-is-fastapi.md) — the framework, the stack, and how its philosophy differs from Django's.
- [Installing FastAPI and your first app](01-getting-started/02-installing-and-first-app.md) — setup and a first typed app, side by side with Django.
- [The dev server](01-getting-started/03-the-dev-server.md) — `fastapi dev` / `uvicorn` vs `runserver`, reload, and workers.
- [Project structure](01-getting-started/04-project-structure.md) — `APIRouter` / `include_router` vs Django apps and `include()`.
- [Application lifespan](01-getting-started/05-application-lifespan.md) — `lifespan` startup/shutdown vs `AppConfig.ready()`.

### Planned topics

The structure below is the working outline for the book — it will grow
into linked articles as each one is written.

1. **Getting started** — what FastAPI is, installing it, your first app, the dev server (`uvicorn` vs `runserver`), project layout without Django's app/project scaffolding, and application lifespan (startup/shutdown, the `AppConfig.ready()` analogue).
2. **Routing and requests** — path operations vs `urls.py`, path and query parameters, request bodies, responses and status codes, error handling and exceptions (`HTTPException`, handlers, the `422` shape), forms and file uploads, and the shift away from class-based views.
3. **Data with Pydantic** — Pydantic models vs Django forms and DRF serializers, validation, `response_model`, and settings (`pydantic-settings` vs `settings.py`).
4. **Templates and static files** — `Jinja2Templates` vs the Django Template Language, `render()` → returning an `HTMLResponse`, and serving static assets vs `collectstatic`.
5. **Databases** — SQLAlchemy + Alembic: models, the session, migrations vs Django migrations, querying, serializing ORM objects with Pydantic (`from_attributes`, the `ModelSerializer` analogue), and async access.
6. **Dependency injection** — `Depends()`, the idea Django has no direct equivalent for; dependencies with `yield`, sub-dependencies, reuse, and what replaces signals.
7. **Authentication** — Django auth/sessions vs OAuth2/JWT, security dependencies, CSRF and the cookie-vs-token model, and CORS.
8. **Middleware** — Starlette middleware vs Django's `MIDDLEWARE` stack.
9. **Async and concurrency** — WSGI vs ASGI, `async def` and when to use it, background tasks vs Celery, and WebSockets vs Django Channels.
10. **Testing** — pytest: `TestClient`, fixtures, and testing dependencies and async code.
11. **The admin gap and deployment** — what replaces `django.contrib.admin`, and deploying Uvicorn workers.

**Appendix — Ecosystem map:** a Django-package → FastAPI-stack cheat-sheet (DRF → FastAPI-native, `django-allauth` → `fastapi-users`, Celery → `arq`/Celery, `django.contrib.admin` → SQLAdmin, `django-filter` → query params, caching, pagination, rate limiting, and packaging).

### Companion projects

Every chapter ships with two small, runnable **companion projects** — one
in **FastAPI** and one in **Django** — that implement exactly the
functionality the chapter describes, with tests proving they work. You can
read the chapter, then download and run both sides to see the same feature
built each way.

## Source

- Source repository: <https://github.com/oduvan/learn-fastapi-from-django>.
- Each conspect cites the official sources it consulted at the bottom of
  the page — typically [fastapi.tiangolo.com](https://fastapi.tiangolo.com/),
  [docs.pydantic.dev](https://docs.pydantic.dev/),
  [starlette.io](https://www.starlette.io/), and
  [docs.djangoproject.com](https://docs.djangoproject.com/).
