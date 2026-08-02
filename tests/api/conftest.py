"""Shared fixtures and helpers for API tests."""

from pathlib import Path

import fitz
import pytest
from fastapi.testclient import TestClient

from main import app
from utils.file_utils import PROCESSED_DIR, UPLOAD_DIR

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_dirs():
    """Ensure upload and processed directories are empty around each test."""
    for d in (UPLOAD_DIR, PROCESSED_DIR):
        for p in d.iterdir():
            p.unlink()
    yield
    for d in (UPLOAD_DIR, PROCESSED_DIR):
        for p in d.iterdir():
            p.unlink()


def pdf_bytes(n_pages: int) -> bytes:
    """Build an n-page blank PDF as raw bytes."""
    doc = fitz.open()
    for _ in range(n_pages):
        doc.new_page(width=200, height=200)
    data = doc.tobytes()
    doc.close()
    return data


def upload(n_pages: int):
    """Return a multipart file tuple for a blank n-page PDF."""
    return ("f.pdf", pdf_bytes(n_pages), "application/pdf")


def num_pages(path: Path) -> int:
    """Return the page count of the PDF at path."""
    with fitz.open(path) as doc:
        return doc.page_count
