"""Custom domain exceptions and HTTP error helpers."""

from typing import NoReturn

from fastapi import HTTPException, status


class PDFError(Exception):
    """Base class for all PDF service errors."""


class UploadTooLargeError(PDFError):
    """Raised when an upload exceeds the configured size limit."""


class UnsupportedContentTypeError(PDFError):
    """Raised when an upload is not a PDF content type."""


class InvalidPDFError(PDFError):
    """Raised when a file cannot be parsed as a PDF."""


def http_400(detail: str) -> NoReturn:
    """Raise an HTTP 400 Bad Request with the given detail."""
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def http_413(detail: str) -> NoReturn:
    """Raise an HTTP 413 Payload Too Large with the given detail."""
    raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=detail)
