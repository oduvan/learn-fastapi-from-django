# learn-fastapi-from-django

Conspect notes for a **Django developer moving to FastAPI** — every topic
explains the FastAPI way and compares it, side by side, with how Django
does the same job. Runnable examples throughout, targeting
**FastAPI 0.139**, **Django 6.0**, and **Python 3.13**.

**Read it as a site:** <https://oduvan.github.io/learn-fastapi-from-django/>

The notes live under [`docs/`](docs/). The site is built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and
deployed by [`.github/workflows/pages.yml`](.github/workflows/pages.yml)
on every push to `master`.

## Local preview

```bash
python3 -m venv .venv-mkdocs
.venv-mkdocs/bin/pip install 'mkdocs-material>=9,<10' mkdocs-static-i18n
.venv-mkdocs/bin/mkdocs serve
```

Then open http://127.0.0.1:8000.
