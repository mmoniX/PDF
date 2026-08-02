"""FastAPI dependencies that ingest uploaded PDFs into temporary files."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from fastapi import File, UploadFile

from exceptions import (
    InvalidPDFError,
    UnsupportedContentTypeError,
    UploadTooLargeError,
    http_400,
    http_413,
)
from utils.file_utils import assert_valid_pdf, cleanup, save_upload


@dataclass
class UploadedPDF:
    """An uploaded PDF saved to disk, with its validated page count."""

    path: Path
    num_pages: int


def _save(file: UploadFile) -> Path:
    """Save an upload to disk, mapping size and content-type errors to HTTP responses."""
    try:
        return save_upload(file)
    except UploadTooLargeError as e:
        http_413(str(e))
    except UnsupportedContentTypeError as e:
        http_400(str(e))


def _validate(path: Path) -> int:
    """Return the page count if path is a parseable PDF, else raise HTTP 400."""
    try:
        return assert_valid_pdf(path)
    except InvalidPDFError as e:
        http_400(str(e))


def ingest_pdf(file: Annotated[UploadFile, File()]) -> Iterator[UploadedPDF]:
    """Yield one validated upload; the temp file is removed after the request."""
    upload_path = _save(file)
    try:
        yield UploadedPDF(upload_path, _validate(upload_path))
    finally:
        cleanup(upload_path)


def ingest_pdfs(files: Annotated[list[UploadFile], File()]) -> Iterator[list[UploadedPDF]]:
    """Yield two or more validated uploads; temp files are removed after the request."""
    if len(files) < 2:
        http_400("Provide at least 2 PDF files")
    upload_paths = [_save(f) for f in files]
    try:
        yield [UploadedPDF(p, _validate(p)) for p in upload_paths]
    finally:
        for p in upload_paths:
            cleanup(p)
