# Project: learn-fastapi-from-django

A personal learning repository. The user is an experienced **Django**
developer picking up **FastAPI**; Claude assists with explanations,
articles (conspects), and runnable example code. The defining feature of
this book is that it is **comparative** — every topic is taught in FastAPI
terms *and* set side by side with the Django equivalent.

## About the user

- Long Django background (years of production experience — the ORM, the
  admin, DRF, class-based views, migrations, the request/response cycle).
- Learning FastAPI (and its stack: Starlette, Pydantic, Uvicorn) from
  scratch.
- Wants FastAPI explained **on its own terms first**, then an explicit
  Django comparison so existing knowledge transfers. The comparison is
  a first-class part of every article, not an afterthought.

## Repository layout

```
learn-fastapi-from-django/
├── CLAUDE.md
├── README.md                        ← short repo intro, points at the site
├── mkdocs.yml                       ← MkDocs Material config
├── .github/workflows/pages.yml      ← builds + deploys to GitHub Pages
└── docs/                            ← MkDocs docs_dir; everything below
    │                                  is what becomes the published site
    ├── index.md                     ← home page
    ├── 01-getting-started/          ← topic 1
    │   ├── 01-what-is-fastapi.md
    │   └── ...
    └── NN-next-topic/
```

- All conspects and runnable examples live **under `docs/`**.
- Each topic gets its own folder named `docs/NN-kebab-case-topic/`
  (two-digit prefix).
- Inside each topic folder, every file is numbered `NN-name.ext` —
  conspect `.md` files and any example `.py` files share one continuous
  sequence so the intended reading order is always clear.
- Runnable multi-file example apps live in subfolders inside the topic
  (e.g. `NN-demo-app/`). Inside those subfolders normal Python project
  conventions apply — the numeric-prefix rule does not.

## Companion projects (one FastAPI + one Django per chapter)

Every chapter ships **two runnable, tested projects** — a FastAPI one and
a Django one — implementing exactly the functionality the chapter
describes. They let a reader run and diff the same feature built each way.

- **Location.** Beside the chapter, in a folder named `NN-demo/` where
  `NN` matches the chapter's number, with two subfolders:
  `NN-demo/fastapi/` and `NN-demo/django/`. Each is a self-contained
  project (its own `requirements.txt`, pinned to the versions this repo
  targets, and a short `README.md` with run + test commands).
- **Excluded from the docs build.** `mkdocs.yml` has an `exclude_docs`
  pattern (`*/**/*-demo/`) so these source trees are never turned into
  doc pages. The chapter's `.md` shows and explains the code; the folder
  holds the runnable copy.
- **Tested before every commit.** Both sides must actually run and pass
  their tests (FastAPI via `pytest` + `TestClient`; Django via
  `manage.py test`) on Python 3.13 before you commit. The two projects
  should expose the **same API** so their tests assert equivalent
  behaviour — including the places where the frameworks legitimately
  differ (e.g. a bad path type is `422` in FastAPI, `404` in Django).
- **Referenced from the chapter.** End (or thread through) each chapter
  with a short "Companion projects" section pointing at the two folders
  and their run/test commands.
- Keep code inside the chapter `.md` in sync with the real project files —
  the prose snippets should be copy-pasted from (or identical to) what's
  in `NN-demo/`, so what the reader reads is what actually runs.

## Workflow

1. **Discuss in chat first.** A new topic starts with conversation —
   the user asks questions; Claude answers them in chat.
2. **Then capture.** When the user is satisfied, they ask Claude to
   "make a note", "create a conspect", or "create an example file".
   Only at that point does Claude write files.
3. **One topic folder per subject.** Create the folder as
   `docs/NN-topic/` up front (so we have a home for notes) without
   pre-populating content. When a new topic folder is created, also:
   - add a `nav:` entry for the topic in `mkdocs.yml`,
   - add a `nav:` entry for each new conspect file inside that topic
     as files are created (titles are user-facing — drop the numeric
     prefix and use Title Case, e.g. `Path and query parameters:
     02-routing-and-requests/02-path-and-query-parameters.md`),
   - add the topic title and every per-file title to the
     `nav_translations:` block of the `uk` locale in `mkdocs.yml` so
     the Ukrainian navigation labels are not left in English.
4. **Every English change is followed by a Ukrainian change.** This
   project ships bilingual (English default, Ukrainian via
   mkdocs-static-i18n). Whenever you create or edit a `docs/.../NN-foo.md`
   article, you must create or update its `docs/.../NN-foo.uk.md`
   companion **in the same commit**. The same applies to `docs/index.md`.
   Quick rules:
   - **New article** → write `NN-foo.md` and `NN-foo.uk.md` together.
   - **Edit to an English article** → port the same edit into the `.uk.md`
     translation in the same commit. Don't let translations drift.
   - **Code blocks**: keep snippets, identifiers, and `# output: ...`
     comments **identical** between languages — only translate the prose
     around them and any natural-language code comments.
   - **Nav labels**: any new English nav label in `mkdocs.yml` needs a
     matching entry in `plugins.i18n.languages[uk].nav_translations`.
   - **`fallback_to_default: true`** keeps the site shippable while a
     translation is in flight — but treat that as the safety net, not
     the workflow.
   - The translation rule applies only to user-facing docs under
     `docs/`. `CLAUDE.md`, `README.md`, the workflow file, and other
     repo-meta files stay English-only.
   - A `ukrainian-translator` subagent exists (`.claude/agents/`) and
     should be used to produce/refresh `.uk.md` files.

## Style of explanations and conspects

- **FastAPI-first, always compared.** Explain the FastAPI rule, syntax,
  and behaviour fully and on its own terms. Then draw the Django
  comparison explicitly — this is a book *for Django developers*, so the
  comparison is expected in every article, not optional flavour.
- **The `> **From Django:**` callout is the primary comparison device.**
  Use it after a FastAPI explanation to say how Django does the same
  thing and where the mental model differs. Where a genuine side-by-side
  helps, show both with tabbed code blocks (`=== "FastAPI"` /
  `=== "Django"`) or two adjacent fenced blocks.
- **Don't assume FastAPI knowledge; do assume Django knowledge.** You can
  reference `settings.py`, `models.py`, `QuerySet`, `manage.py`, the
  admin, DRF serializers, middleware, and migrations without explaining
  them. Explain every FastAPI/Starlette/Pydantic concept from zero.
- **Code examples are mandatory.** Every concept ships with at least one
  small runnable snippet in a fenced ```python block. Show expected
  behaviour as a `# output: ...` comment, or the HTTP request/response
  where that's the point. Use `# error: ...` to label snippets that
  intentionally fail.
- **Source-verified.** Verify facts against the official docs
  (fastapi.tiangolo.com, docs.pydantic.dev, www.starlette.io,
  docs.djangoproject.com) before writing. End every article with a
  `## Sources` section listing the URLs consulted as markdown links.
- **Run the code, don't just claim it.** Doc-reading alone is not enough.
  Every non-trivial snippet must be executed in a throwaway venv to
  confirm the actual output, validation errors, and status codes match
  the prose. Treat runtime verification as a required step, not polish.
- **GitHub-flavoured Markdown.** Fenced code blocks with language tags
  (```python, ```bash, ```http), tables, and standard headings.

## Tooling and versions

- The materials target **FastAPI 0.139.x**, **Starlette** and
  **Pydantic v2** as pulled in by that FastAPI release, **Uvicorn** as
  the ASGI server, **Django 6.0.x**, and **Python 3.13**.
- Write everything as present-tense fact for these versions. Do not
  annotate features with "since FastAPI 0.x" / "added in Django X"
  unless the article is specifically about version/compatibility
  mechanics.
- FastAPI is pre-1.0 (0.x): pin exact versions in examples and mention
  that minor releases can carry breaking changes where it's relevant.

## Published site (GitHub Pages)

- Source repo: <https://github.com/oduvan/learn-fastapi-from-django>.
- Published URL: <https://oduvan.github.io/learn-fastapi-from-django/>.
- Static-site generator: **MkDocs Material** (`mkdocs-material>=9,<10`)
  plus `mkdocs-static-i18n`, configured in `mkdocs.yml`.
- The build runs in `.github/workflows/pages.yml` on every push to
  `master`. It executes `mkdocs build --strict` (so broken intra-doc
  links or missing nav entries fail CI), then deploys via
  `actions/deploy-pages@v4`. The repo's **Settings → Pages → Source**
  must be set to **"GitHub Actions"** for the deploy step to take.
- Local preview: create a venv, `pip install 'mkdocs-material>=9,<10'
  mkdocs-static-i18n`, then `mkdocs serve` for live reload on
  http://127.0.0.1:8000.
- The `site/` directory (build output) and `.venv*/` are in
  `.gitignore`. Don't commit them.
