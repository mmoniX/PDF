# AGENTS.md

- follow deduplicated, optimal, lean, without redundency, lean coding style.
- avoid lazy import and nested defination
- have meaningfull concise docstring for both functions and files
- update README file after meaningfull changes


## Project
- FastAPI PDF service. Entrypoint: `main.py` (imports `api.routers.edit` and `api.routers.files`). Layers: `api/routers/` handlers + `api/deps.py` (upload ingestion) → `services/` logic → `utils/` helpers; `schemas/` holds Pydantic response models.
- Planned AI features (`services/pdf_summary.py`, `services/pdf_translate.py`, `services/pdf_convert.py`) are empty stubs; `openai` is declared but unused.

## Commands
- Package manager is `uv` (venv `.venv`). Install: `uv sync`. Tests: `uv run pytest`.
- Lint: `uv run ruff check .`; format: `uv run ruff format .` (config in `pyproject.toml`, line length 100).
- Run the API: `uv run uvicorn main:app --reload`.

## Gotchas
- PyMuPDF (`import fitz`) is the only PDF library — use it for both editing and text extraction. Do not add pypdf/pdfplumber; PyMuPDF's `delete_pages` takes 0-based indices, all other methods are 1-based.
- Custom exceptions and HTTP helpers (`http_400`/`http_413`) live in top-level `exceptions.py`; `api/deps.py` maps domain exceptions to them.
- `utils/file_utils.py` creates gitignored `data/uploads/` and `data/processed/` at import time; uploads are auto-deleted after processing, processed outputs persist and are served by `GET /pdf/files/{filename}`.
- `PDFService` methods are `@staticmethod`; call as `PDFService.split(...)` without instantiating.
- Page indices are 1-based inclusive everywhere. Range checks live in handlers; upload ingestion + parseability live in `api/deps.py` (`ingest_pdf` / `ingest_pdfs` yield `UploadedPDF` and clean up temp files).
- Uploads capped at 50 MB (`MAX_UPLOAD_SIZE`); content-type + parseability checked before processing.
- Never name a `tests/` subdirectory after a top-level package (e.g. `tests/api/`): pytest prepends `tests/` to `sys.path`, shadowing the real `api` package. Test dirs need no `__init__.py`.
