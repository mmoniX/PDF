from tests.api.conftest import client, num_pages, upload
from utils.file_utils import PROCESSED_DIR, UPLOAD_DIR


def test_split():
    res = client.post("/pdf/split?start=2&end=3", files={"file": upload(5)})
    assert res.status_code == 200
    assert num_pages(PROCESSED_DIR / res.json()["output_file"]) == 2


def test_split_invalid_range():
    res = client.post("/pdf/split?start=2&end=6", files={"file": upload(5)})
    assert res.status_code == 400


def test_merge():
    res = client.post(
        "/pdf/merge",
        files=[("files", upload(2)), ("files", upload(3))],
    )
    assert res.status_code == 200
    assert num_pages(PROCESSED_DIR / res.json()["output_file"]) == 5


def test_merge_single_file_rejected():
    res = client.post("/pdf/merge", files=[("files", upload(2))])
    assert res.status_code == 400


def test_delete_pages():
    res = client.post("/pdf/delete-pages", files={"file": upload(5)}, params={"pages": [2, 4]})
    assert res.status_code == 200
    assert num_pages(PROCESSED_DIR / res.json()["output_file"]) == 3


def test_reorder():
    res = client.post("/pdf/reorder", files={"file": upload(3)}, params={"order": [3, 1, 2]})
    assert res.status_code == 200
    assert num_pages(PROCESSED_DIR / res.json()["output_file"]) == 3


def test_wrong_content_type_rejected():
    res = client.post(
        "/pdf/split?start=1&end=1",
        files={"file": ("f.txt", b"not a pdf", "text/plain")},
    )
    assert res.status_code == 400


def test_garbage_pdf_with_pdf_content_type_rejected():
    res = client.post(
        "/pdf/split?start=1&end=1",
        files={"file": ("f.pdf", b"not actually a pdf", "application/pdf")},
    )
    assert res.status_code == 400


def test_upload_cleaned_up():
    client.post("/pdf/split?start=1&end=2", files={"file": upload(3)})
    assert not any(UPLOAD_DIR.iterdir())
