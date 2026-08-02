"""Filesystem helpers: upload storage, PDF validation, and cleanup."""

import uuid
from pathlib import Path

import fitz
from fastapi import UploadFile

from exceptions import InvalidPDFError, UnsupportedContentTypeError, UploadTooLargeError

UPLOAD_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")

MAX_UPLOAD_SIZE = 50 * 1024 * 1024

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf"}


def generate_filename(suffix: str = ".pdf") -> str:
    """Return a random filename carrying the given suffix."""
    return f"{uuid.uuid4()}{suffix}"


def save_upload(file: UploadFile) -> Path:
    """Stream an upload into UPLOAD_DIR, rejecting bad content types and oversize files."""
    if file.content_type not in PDF_CONTENT_TYPES:
        raise UnsupportedContentTypeError("Only PDF files are supported")

    path = UPLOAD_DIR / generate_filename()
    size = 0
    with open(path, "wb") as f:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_SIZE:
                raise UploadTooLargeError("Upload exceeds the 50 MB limit")
            f.write(chunk)
    return path


def assert_valid_pdf(path: Path) -> int:
    """Return the page count if path is a readable PDF, else raise InvalidPDFError."""
    try:
        with fitz.open(path) as doc:
            return doc.page_count
    except Exception as e:
        raise InvalidPDFError("Unable to read PDF file") from e


def cleanup(path: Path):
    """Best-effort deletion of a temporary file."""
    path.unlink(missing_ok=True)
