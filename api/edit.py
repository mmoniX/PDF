from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path
from pypdf import PdfReader

from services.pdf_edit import PDFService
from utils.file_utils import (
    UPLOAD_DIR,
    PROCESSED_DIR,
    generate_filename,
)

router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post("/split")
async def split_pdf(
    file: UploadFile = File(...),
    start: int = 1,
    end: int = 1,
):
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    input_path = UPLOAD_DIR / generate_filename()
    output_path = PROCESSED_DIR / generate_filename()

    with open(input_path, "wb") as f:
        f.write(await file.read())

    if start < 1 or end < start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid page range: ensure 1 <= start <= end",
        )

    try:
        num_pages = len(PdfReader(input_path).pages)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to read PDF file",
        )

    if end > num_pages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page range exceeds document length ({num_pages} pages)",
        )

    PDFService.split(input_path, start, end, output_path)

    return {"output_file": output_path.name}
