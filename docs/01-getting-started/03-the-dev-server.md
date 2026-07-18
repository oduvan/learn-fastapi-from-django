# The dev server

FastAPI doesn't run itself. A FastAPI app is an ASGI *application* — an
object — and something has to actually open a socket, speak HTTP, and hand
requests to it. That something is an ASGI **server**, almost always
[Uvicorn](https://www.uvicorn.org/). This chapter covers how you run your
app while developing.

## `fastapi dev` — the batteries-included way

If you installed `fastapi[standard]`, you have the `fastapi` CLI. `fastapi
dev` is the development command:

```bash
fastapi dev main.py
```

It finds the `FastAPI` instance in `main.py`, starts Uvicorn with
**auto-reload on**, binds `127.0.0.1:8000`, and prints where the app and
the interactive docs are:

```
Serving at: http://127.0.0.1:8000
API docs:   http://127.0.0.1:8000/docs
```

Edit a file, save, and the server restarts automatically.

## `uvicorn` — the underlying command

`fastapi dev` is a convenience wrapper. Underneath it's just Uvicorn, and
you can call Uvicorn directly — this is what most projects put in their
scripts:

```bash
uvicorn main:app --reload
```

`main:app` is `module:variable` — the `app` object in `main.py`. Useful
flags:

```bash
uvicorn main:app --reload                       # dev: auto-reload on
uvicorn main:app --host 0.0.0.0 --port 9000     # bind all interfaces, port 9000
uvicorn main:app --reload --reload-dir app      # only watch ./app for changes
uvicorn main:app --log-level debug              # noisier logs
```

Defaults worth knowing: host `127.0.0.1`, port `8000`, reload **off**
(that's why `--reload` is explicit here, whereas `fastapi dev` turns it on
for you).

> **From Django:** `uvicorn main:app --reload` is the direct counterpart of
> `python manage.py runserver` — a local HTTP server with a file watcher
> that restarts on save. `manage.py runserver` also defaults to
> `127.0.0.1:8000`, and takes the address the same way you'd expect:
> `runserver 0.0.0.0:9000`. Auto-reload is on by default there too;
> `--noreload` turns it off (the equivalent of plain `uvicorn` with no
> `--reload`).

## Running "for real": `fastapi run` and workers

Here is the part that surprises Django developers. `manage.py runserver`
is a **development-only** server — the Django docs tell you, in bold, never
to use it in production. Uvicorn is different: it *is* a production ASGI
server. The dev and prod commands are just different profiles of the same
program.

```bash
fastapi run main.py                 # prod profile: no reload, binds 0.0.0.0
fastapi run main.py --workers 4     # 4 worker processes

# the Uvicorn equivalent:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

`--workers N` runs N independent worker processes to use multiple CPU
cores. (Auto-reload and multiple workers don't combine — reload runs a
single process.)

> **From Django:** In the Django world, the dev server and the production
> server are two different programs: you develop with `runserver` and
> deploy behind Gunicorn or uWSGI (WSGI), or Uvicorn/Daphne (ASGI). With
> FastAPI there's no throwaway dev server to leave behind — you run Uvicorn
> in both places, flipping `--reload` off and `--workers` up for
> production. Multi-process scaling that Django hands to Gunicorn
> (`gunicorn --workers 4`) is `uvicorn --workers 4` here. Deployment gets
> its own chapter later; the point now is that the server is the same one.

## A note on the reloader

The auto-reloader watches your source files and restarts the server
process on change. It is a **development** feature in both frameworks —
turn it off in production (it adds overhead and a file-watching thread).
`fastapi run` and `uvicorn --workers` already leave it off; with
`runserver` you'd pass `--noreload`.

One thing `runserver` does that Uvicorn does not: serve your static files
automatically in `DEBUG` mode. FastAPI has no static-file handling until
you add it — that's covered in the *Templates and static files* chapter.

## Companion projects { #companion-projects }

A minimal app, built both ways, under this chapter's `03-demo/` folder:

- `03-demo/fastapi/` ([download](03-demo-fastapi.zip)) — run with
  `fastapi dev main.py`; test with `pytest`.
- `03-demo/django/` ([download](03-demo-django.zip)) — run with
  `python manage.py runserver`; test with `python manage.py test`.

To keep them honest about *serving*, each test suite includes one test
that boots the **real** server over HTTP — Uvicorn in a subprocess on the
FastAPI side, `manage.py runserver` in a subprocess on the Django side —
and makes an actual HTTP request, rather than only using the in-process
test client.

## Sources

- [FastAPI — Run a server manually (Uvicorn)](https://fastapi.tiangolo.com/deployment/manually/)
- [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/)
- [Uvicorn — settings and command line](https://www.uvicorn.org/settings/)
- [Django — runserver](https://docs.djangoproject.com/en/6.0/ref/django-admin/#runserver)
- [Django — Deploying (why not runserver)](https://docs.djangoproject.com/en/6.0/howto/deployment/)
