# PDF Service

FastAPI service for manipulating PDF files over HTTP: split, merge, delete pages, and reorder.

## Features

- **Split** a PDF by page range
- **Merge** multiple PDFs into one
- **Delete** specific pages
- **Reorder** pages
- Every operation returns a downloadable result file

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) — the only PDF library used
- Pydantic for response models
- Python 3.12, managed with [uv](https://docs.astral.sh/uv/)

## Getting started

```bash
uv sync                # install dependencies into .venv
uv run uvicorn main:app --reload   # start the API at http://127.0.0.1:8000
```

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## API

All endpoints are prefixed with `/pdf`. Page indices are **1-based, inclusive**.

| Method | Path                  | Description                                   |
| ------ | --------------------- | --------------------------------------------- |
| POST   | `/pdf/split`          | `?start=&end=` — extract a page range         |
| POST   | `/pdf/merge`          | upload 2+ PDFs, concatenate in order          |
| POST   | `/pdf/delete-pages`   | `?pages=` (repeatable) — remove pages         |
| POST   | `/pdf/reorder`        | `?order=` (repeatable) — set page order       |
| GET    | `/pdf/files/{name}`   | download a processed output file              |

Uploads are limited to 50 MB and must be `application/pdf`.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/pdf/split?start=2&end=4" \
  -F "file=@report.pdf;type=application/pdf"
# {"output_file": "a1b2c3d4-....pdf"}

curl -OJ "http://127.0.0.1:8000/pdf/files/a1b2c3d4-....pdf"
```

## Project structure

```
main.py            app entrypoint (registers routers)
api/               HTTP layer: deps.py (upload ingestion) + routers
schemas/           Pydantic response models
services/          business logic (pdf_edit.py; summary/translate/convert planned)
utils/             file storage helpers
exceptions.py      custom domain exceptions
tests/             pytest suites (service + API)
```

## Development

```bash
uv run pytest            # run tests
uv run ruff check .      # lint
uv run ruff format .     # format (line length 100)
```
