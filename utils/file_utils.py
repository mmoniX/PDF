import uuid
from pathlib import Path

UPLOAD_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def generate_filename(suffix=".pdf") -> str:
    return f"{uuid.uuid4()}{suffix}"
