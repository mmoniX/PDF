from pathlib import Path

from tests.api.conftest import client, num_pages, upload
from utils.file_utils import PROCESSED_DIR


def test_download_roundtrip():
    name = client.post("/pdf/split?start=2&end=3", files={"file": upload(5)}).json()["output_file"]

    dl = client.get(f"/pdf/files/{name}")
    assert dl.status_code == 200
    assert dl.headers["content-type"] == "application/pdf"
    assert num_pages(Path(PROCESSED_DIR / name)) == 2


def test_path_traversal_blocked():
    res = client.get("/pdf/files/..%2F..%2Fpyproject.toml")
    assert res.status_code == 404


def test_missing_file_404():
    assert client.get("/pdf/files/nope.pdf").status_code == 404
