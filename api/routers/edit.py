"""PDF editing endpoints: split, merge, delete pages, and reorder."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.deps import UploadedPDF, ingest_pdf, ingest_pdfs
from exceptions import http_400
from schemas import ProcessedFile
from services.pdf_edit import PDFService
from utils.file_utils import PROCESSED_DIR, generate_filename

router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post("/split", response_model=ProcessedFile)
def split_pdf(
    pdf: Annotated[UploadedPDF, Depends(ingest_pdf)],
    start: Annotated[int, Query(ge=1)],
    end: Annotated[int, Query(ge=1)],
):
    """Extract pages start..end (inclusive) of the uploaded PDF into a new file."""
    if end < start or end > pdf.num_pages:
        http_400(f"Invalid page range: ensure 1 <= start <= end <= {pdf.num_pages}")
    output_path = PROCESSED_DIR / generate_filename()
    PDFService.split(pdf.path, start, end, output_path)
    return ProcessedFile(output_file=output_path.name)


@router.post("/merge", response_model=ProcessedFile)
def merge_pdfs(pdfs: Annotated[list[UploadedPDF], Depends(ingest_pdfs)]):
    """Concatenate the uploaded PDFs, in order, into a single new file."""
    output_path = PROCESSED_DIR / generate_filename()
    PDFService.merge([p.path for p in pdfs], output_path)
    return ProcessedFile(output_file=output_path.name)


@router.post("/delete-pages", response_model=ProcessedFile)
def delete_pages(
    pdf: Annotated[UploadedPDF, Depends(ingest_pdf)],
    pages: Annotated[list[int], Query()],
):
    """Remove the given 1-based pages from the uploaded PDF."""
    to_delete = set(pages)
    if not to_delete or any(p < 1 or p > pdf.num_pages for p in to_delete):
        http_400(f"Invalid page numbers: ensure 1 <= page <= {pdf.num_pages}")
    output_path = PROCESSED_DIR / generate_filename()
    PDFService.delete_pages(pdf.path, to_delete, output_path)
    return ProcessedFile(output_file=output_path.name)


@router.post("/reorder", response_model=ProcessedFile)
def reorder_pages(
    pdf: Annotated[UploadedPDF, Depends(ingest_pdf)],
    order: Annotated[list[int], Query()],
):
    """Reorder the uploaded PDF's pages per the given 1-based order."""
    if not order or any(p < 1 or p > pdf.num_pages for p in order):
        http_400(f"Invalid page order: ensure 1 <= page <= {pdf.num_pages}")
    output_path = PROCESSED_DIR / generate_filename()
    PDFService.reorder(pdf.path, order, output_path)
    return ProcessedFile(output_file=output_path.name)
