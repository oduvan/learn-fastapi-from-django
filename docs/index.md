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

### Planned topics

The structure below is the working outline for the book — it will grow
into linked articles as each one is written.

1. **Getting started** — what FastAPI is, installing it, your first app, the dev server (`uvicorn` vs `runserver`), and how you lay out a project without Django's app/project scaffolding.
2. **Routing and requests** — path operations vs `urls.py`, path and query parameters, request bodies, responses and status codes, forms and file uploads.
3. **Data with Pydantic** — Pydantic models vs Django forms and DRF serializers, validation, `response_model`, and settings management.
4. **Databases** — choosing an ORM (Django ORM vs SQLAlchemy / SQLModel), models and migrations (Alembic vs Django migrations), querying, and async database access.
5. **Dependency injection** — `Depends()`, the idea Django has no direct equivalent for; dependencies with `yield`, sub-dependencies, and reuse.
6. **Auth and middleware** — Django auth/sessions vs OAuth2/JWT, security dependencies, middleware, and CORS.
7. **Async and concurrency** — WSGI vs ASGI, `async def` and when to use it, background tasks vs Celery.
8. **Testing** — `TestClient` vs Django's test client, pytest patterns, testing dependencies and async code.
9. **From Django's batteries to a FastAPI stack** — the admin gap, templates and static files, and deployment.

## Source

- Source repository: <https://github.com/oduvan/learn-fastapi-from-django>.
- Each conspect cites the official sources it consulted at the bottom of
  the page — typically [fastapi.tiangolo.com](https://fastapi.tiangolo.com/),
  [docs.pydantic.dev](https://docs.pydantic.dev/),
  [starlette.io](https://www.starlette.io/), and
  [docs.djangoproject.com](https://docs.djangoproject.com/).
