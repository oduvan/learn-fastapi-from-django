"""MkDocs hook: package each chapter's companion projects as downloadable
zip archives at build time.

For every ``docs/**/NN-demo/<project>/`` folder (the runnable FastAPI and
Django projects that accompany a chapter, excluded from the docs build by
``exclude_docs``), this produces a sibling archive next to the chapter:

    docs/01-getting-started/02-demo/fastapi/   ->   .../02-demo-fastapi.zip
    docs/01-getting-started/02-demo/django/    ->   .../02-demo-django.zip

The archives are registered as MkDocs ``File`` objects, so:

* they land in the built ``site/`` (and in the per-language subtrees the
  i18n plugin builds), and
* relative links to them from a chapter page validate under
  ``mkdocs build --strict``.

A chapter links to its archives with a plain relative link, e.g.
``[FastAPI project](02-demo-fastapi.zip)``.

No zip files are committed to the repo — they exist only in the build
output.
"""
from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path

from mkdocs.structure.files import File

# Directory names and suffixes that must never end up inside an archive.
_SKIP_DIRS = {
    "__pycache__",
    ".venv",
    ".venv-mkdocs",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
}
_SKIP_SUFFIXES = {".pyc", ".pyo", ".sqlite3", ".db"}

_tmp_root: Path | None = None


def _iter_project_files(project: Path):
    for path in sorted(project.rglob("*")):
        if not path.is_file():
            continue
        parts = set(path.relative_to(project).parts)
        if parts & _SKIP_DIRS:
            continue
        if path.suffix in _SKIP_SUFFIXES:
            continue
        yield path


def _build_zip(project: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # A stable timestamp keeps archives reproducible across builds.
    date_time = (2020, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in _iter_project_files(project):
            arcname = Path(project.name) / path.relative_to(project)
            info = zipfile.ZipInfo(str(arcname), date_time=date_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def _project_archives(docs_dir: Path):
    """Yield (zip_rel, project_dir) for every companion project."""
    for demo in sorted(docs_dir.glob("**/*-demo")):
        if not demo.is_dir():
            continue
        for project in sorted(p for p in demo.iterdir() if p.is_dir()):
            zip_rel = demo.parent.relative_to(docs_dir) / f"{demo.name}-{project.name}.zip"
            yield zip_rel, project


def on_files(files, config):
    global _tmp_root
    docs_dir = Path(config["docs_dir"])
    if _tmp_root is None:
        _tmp_root = Path(tempfile.mkdtemp(prefix="mkdocs-companion-zips-"))

    for zip_rel, project in _project_archives(docs_dir):
        zip_abs = _tmp_root / zip_rel
        _build_zip(project, zip_abs)
        files.append(
            File(
                str(zip_rel),
                str(_tmp_root),
                config["site_dir"],
                config["use_directory_urls"],
            )
        )
    return files


def on_post_build(config):
    """Copy each archive into every localized subtree.

    ``on_files`` registers the archive (so relative links from a chapter
    validate under --strict) and writes it to the default-language root.
    The mkdocs-static-i18n plugin builds each non-default language into a
    ``site/<locale>/`` subtree that mirrors the docs structure but does not
    carry these hook-added files, so fan them out here: any immediate
    subdirectory of the site that mirrors a chapter's folder gets its own
    copy of the archive next to that chapter.
    """
    site_dir = Path(config["site_dir"])
    docs_dir = Path(config["docs_dir"])

    archives = list(_project_archives(docs_dir))
    for zip_rel, project in archives:
        root_zip = site_dir / zip_rel
        if not root_zip.exists():
            _build_zip(project, root_zip)

    for child in sorted(p for p in site_dir.iterdir() if p.is_dir()):
        for zip_rel, _project in archives:
            # A localized subtree mirrors the chapter's folder; other site
            # dirs (assets, search, …) don't, so they're skipped.
            if (child / zip_rel.parent).is_dir():
                dest = child / zip_rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(root_zip, dest)
