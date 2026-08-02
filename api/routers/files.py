"""Serving of processed output files."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from utils.file_utils import PROCESSED_DIR

router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.get("/files/{filename}")
async def download_file(filename: str):
    """Return a processed PDF from disk, blocking any path traversal attempt."""
    path = (PROCESSED_DIR / filename).resolve()
    if not path.is_relative_to(PROCESSED_DIR.resolve()) or not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=filename)
